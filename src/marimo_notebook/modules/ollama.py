from __future__ import annotations
from typing import Iterator, Optional, List
from llm import Model, Prompt, Response, Conversation
import ollama

class OllamaModel(Model):
    """
    A model class for interacting with the Ollama API.
    """
    model_id: str
    needs_key: str = None  # Ollama doesn't need an API key
    key_env_var: str = None
    can_stream: bool = True

    def __init__(self, model_id: str = "mistral", **kwargs):
        """
        Initialize the OllamaModel.

        Args:
            model_id: The ID of the Ollama model to use.
            **kwargs: Additional keyword arguments.
        """
        self.model_id = model_id
        super().__init__(**kwargs)

    def execute(
        self,
        prompt: Prompt,
        stream: bool,
        response: Response,
        conversation: Optional[Conversation],
    ) -> Iterator[str]:
        """
        Execute a prompt using the Ollama model.

        Args:
            prompt: The Prompt object containing the prompt text.
            stream: Whether to stream the response.
            response: The Response object to populate.
            conversation: The Conversation context, if any.

        Yields:
            Generated text from the model.
        """
        messages = []
        if prompt.system:
            messages.append({"role": "system", "content": prompt.system})
        
        # Handle conversation history if present
        if conversation and conversation.messages:
            for msg in conversation.messages:
                role = "assistant" if msg.type == "response" else "user"
                messages.append({"role": role, "content": msg.prompt.prompt})

        # Add the current prompt
        messages.append({"role": "user", "content": prompt.prompt})

        # Access options directly instead of using .get()
        options = {
            "temperature": getattr(prompt.options, "temperature", 0.7),
            "num_predict": getattr(prompt.options, "max_tokens", None),
            "top_p": getattr(prompt.options, "top_p", 1.0),
        }

        try:
            completion = ollama.chat(
                model=self.model_id,
                messages=messages,
                stream=stream,
                options=options,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to generate completion for model '{self.model_id}': {e}")

        if stream:
            for chunk in completion:
                if chunk.get("message", {}).get("content"):
                    yield chunk["message"]["content"]
        else:
            yield completion["message"]["content"]

    @classmethod
    def get_supported_models(cls) -> List[str]:
        """
        Retrieve a list of supported Ollama model names.

        Returns:
            A list of model names supported by the Ollama API.
        """
        try:
            models_data = ollama.list().get('models', [])
            return [model['name'] for model in models_data]
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve supported models: {e}")

class Options(Model.Options):
    """
    Options for configuring the Ollama model behavior.
    """
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    top_p: Optional[float] = 1.0
    # Add other Ollama-specific parameters as needed

def get_model(model_name: str) -> OllamaModel:
    """
    Get an Ollama model instance by name.
    
    Args:
        model_name: Name of the Ollama model to use (e.g., "mistral", "llama2")
    
    Returns:
        OllamaModel: An instance of OllamaModel configured for the specified model
    
    Raises:
        ValueError: If the model name is not recognized
    """
    supported_models = OllamaModel.get_supported_models()
    if model_name not in supported_models:
        raise ValueError(
            f"Unknown model: {model_name}. "
            f"Supported models are: {', '.join(supported_models)}"
        )
    return OllamaModel(model_id=model_name)



