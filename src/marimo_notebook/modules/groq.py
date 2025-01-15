from __future__ import annotations  # For forward references in type hints
from typing import Iterator, Optional, Dict, Type, List
from llm import Model, Prompt, Response, Conversation
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

class GroqModel(Model):
    """
    A model class for interacting with the Groq API using specified models.
    """

    model_id: str
    needs_key: str = "Groq API key"
    key_env_var: str = "GROQ_API_KEY"
    can_stream: bool = True

    def __init__(self, model_id: str = "mixtral-8x7b-32768", **kwargs):
        """
        Initialize the GroqModel.

        Args:
            model_id: The ID of the Groq model to use.
            **kwargs: Additional keyword arguments.
        """
        self.model_id = model_id
        self.client = None
        super().__init__(**kwargs)

    def _ensure_client(self):
        """
        Ensure the Groq client is initialized.
        """
        if self.client is None:
            if not self.key:
                raise ValueError("Groq API key is required")
            try:
                self.client = Groq(api_key=self.key)
            except Exception as e:
                raise RuntimeError(f"Failed to initialize Groq client: {e}")

    def execute(
        self,
        prompt: Prompt,
        stream: bool,
        response: Response,
        conversation: Optional[Conversation],
    ) -> Iterator[str]:
        """
        Execute a prompt using the Groq model.

        Args:
            prompt: The Prompt object containing the prompt text.
            stream: Whether to stream the response.
            response: The Response object to populate.
            conversation: The Conversation context, if any.

        Yields:
            Generated text from the model.
        """
        self._ensure_client()

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

        try:
            completion = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                stream=stream,
                temperature= getattr(prompt.options, "temperature", 0.7),
                max_tokens= getattr(prompt.options, "max_tokens", None),
            )
        except Exception as e:
            raise RuntimeError(f"Failed to generate completion: {e}")

        if stream:
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        else:
            yield completion.choices[0].message.content

        # Store usage information if available
        usage = getattr(completion, "usage", None)
        if usage:
            response.prompt_tokens = usage.prompt_tokens
            response.completion_tokens = usage.completion_tokens

    def close(self):
        """
        Close the Groq client and release any resources.
        """
        if self.client:
            self.client.close()
            self.client = None

    def __enter__(self):
        self._ensure_client()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @classmethod
    def get_supported_models(cls) -> List[str]:
        """
        Retrieve a list of supported Groq model IDs.

        Returns:
            A list of model IDs supported by the Groq API.
        """
        key = os.getenv(cls.key_env_var)
        if not key:
            raise ValueError("Groq API key is required to retrieve supported models")
        try:
            client = Groq(api_key=key)
            models = [model.id for model in client.models.list().data]
            client.close()
            return models
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve supported models: {e}")

class Options(Model.Options):
    """
    Options for configuring the Groq model behavior.
    """
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    top_p: Optional[float] = 1.0
    # Add other Groq-specific parameters as needed

def get_model(model_name: str) -> GroqModel:
    """
    Get a Groq model instance by name.
    
    Args:
        model_name: Name of the Groq model to use (e.g., "mixtral-8x7b-32768", "llama2-70b-4096")
    
    Returns:
        GroqModel: An instance of GroqModel configured for the specified model
    
    Raises:
        ValueError: If the model name is not recognized
    """
    supported_models = GroqModel.get_supported_models()
    if model_name not in supported_models:
        raise ValueError(
            f"Unknown model: {model_name}. "
            f"Supported models are: {', '.join(supported_models)}"
        )
    return GroqModel(model_id=model_name)



