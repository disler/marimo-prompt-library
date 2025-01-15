import llm
from dotenv import load_dotenv
import os
from mako.template import Template
from .groq import get_model as get_groq_model
from .ollama import get_model as get_ollama_model

# Load environment variables from .env file
load_dotenv()


def conditional_render(prompt, context, start_delim="% if", end_delim="% endif"):
    template = Template(prompt)
    return template.render(**context)


def parse_markdown_backticks(str) -> str:
    if "```" not in str:
        return str.strip()
    # Remove opening backticks and language identifier
    str = str.split("```", 1)[-1].split("\n", 1)[-1]
    # Remove closing backticks
    str = str.rsplit("```", 1)[0]
    # Remove any leading or trailing whitespace
    return str.strip()


def prompt(model: llm.Model, prompt: str, **kwargs) -> str:
    """
    Send a prompt to a language model and return the response.
    
    Args:
        model: The language model to use
        prompt: The prompt text
        **kwargs: Additional arguments to pass to the model's prompt method
    
    Returns:
        str: The model's response
    """
    # Set stream=False by default if not specified
    kwargs.setdefault('stream', False)
    
    # Get the response from the model
    response = model.prompt(prompt, **kwargs)
    
    # Handle the response based on streaming mode
    if kwargs.get('stream', False):
        return response
    else:
        # Join all chunks into a single string
        return ''.join(chunk for chunk in response)


def prompt_with_temp(model: llm.Model, prompt: str, temperature: float = 0.7):
    """
    Send a prompt to the model with a specified temperature.

    Args:
    model (llm.Model): The LLM model to use.
    prompt (str): The prompt to send to the model.
    temperature (float): The temperature setting for the model's response. Default is 0.7.

    Returns:
    str: The model's response text.
    """

    model_id = model.model_id
    if "o1" in model_id or "gemini" in model_id:
        temperature = 1
        res = model.prompt(prompt, stream=False)
        return res.text()

    res = model.prompt(prompt, stream=False, temperature=temperature)
    return res.text()


def get_model_name(model: llm.Model):
    return model.model_id


def build_sonnet_3_5():
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    sonnet_3_5_model: llm.Model = llm.get_model("claude-3.5-sonnet")
    sonnet_3_5_model.key = ANTHROPIC_API_KEY

    return sonnet_3_5_model


def build_mini_model():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    gpt4_o_mini_model: llm.Model = llm.get_model("gpt-4o-mini")
    gpt4_o_mini_model.key = OPENAI_API_KEY
    return gpt4_o_mini_model


def build_big_3_models():
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    sonnet_3_5_model: llm.Model = llm.get_model("claude-3.5-sonnet")
    sonnet_3_5_model.key = ANTHROPIC_API_KEY

    gpt4_o_model: llm.Model = llm.get_model("4o")
    gpt4_o_model.key = OPENAI_API_KEY

    gemini_1_5_pro_model: llm.Model = llm.get_model("gemini-1.5-pro-latest")
    gemini_1_5_pro_model.key = GEMINI_API_KEY

    return sonnet_3_5_model, gpt4_o_model, gemini_1_5_pro_model


def build_latest_openai():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # chatgpt_4o_latest_model: llm.Model = llm.get_model("chatgpt-4o-latest") - experimental
    chatgpt_4o_latest_model: llm.Model = llm.get_model("gpt-4o")
    chatgpt_4o_latest_model.key = OPENAI_API_KEY
    return chatgpt_4o_latest_model


def build_big_3_plus_mini_models():

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    sonnet_3_5_model: llm.Model = llm.get_model("claude-3.5-sonnet")
    sonnet_3_5_model.key = ANTHROPIC_API_KEY

    gpt4_o_model: llm.Model = llm.get_model("4o")
    gpt4_o_model.key = OPENAI_API_KEY

    gemini_1_5_pro_model: llm.Model = llm.get_model("gemini-1.5-pro-latest")
    gemini_1_5_pro_model.key = GEMINI_API_KEY

    gpt4_o_mini_model: llm.Model = llm.get_model("gpt-4o-mini")
    gpt4_o_mini_model.key = OPENAI_API_KEY

    chatgpt_4o_latest_model = build_latest_openai()

    return (
        sonnet_3_5_model,
        gpt4_o_model,
        gemini_1_5_pro_model,
        gpt4_o_mini_model,
    )


def build_gemini_duo():
    gemini_1_5_pro: llm.Model = llm.get_model("gemini-1.5-pro-latest")
    gemini_1_5_flash: llm.Model = llm.get_model("gemini-1.5-flash-latest")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    gemini_1_5_pro.key = GEMINI_API_KEY
    gemini_1_5_flash.key = GEMINI_API_KEY

    return gemini_1_5_pro, gemini_1_5_flash


def build_ollama_models():
    mistral_model: llm.Model = get_ollama_model("mistral:latest")
    phi4_14b_model: llm.Model = get_ollama_model("phi4:latest")
    llama3_2_model: llm.Model = get_ollama_model("llama3.2:latest")
    return mistral_model, phi4_14b_model, llama3_2_model

def build_groq_models():
    groq_api_key = os.getenv("GROQ_API_KEY")
    llama_3_3_70b_versatile_model: llm.Model = get_groq_model("llama-3.3-70b-versatile")
    llama_3_3_70b_versatile_model.key = groq_api_key
    return llama_3_3_70b_versatile_model

def build_ollama_slm_models():
    llama3_2_model: llm.Model = llm.get_model("mistral:latest")

    return [llama3_2_model]


def build_openai_model_stack():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    gpt4_o_mini_model: llm.Model = llm.get_model("gpt-4o-mini")
    gpt4_o_2024_08_06_model: llm.Model = llm.get_model("gpt-4o")
    o1_preview_model: llm.Model = llm.get_model("o1-preview")
    o1_mini_model: llm.Model = llm.get_model("o1-mini")

    models = [
        gpt4_o_mini_model,
        gpt4_o_2024_08_06_model,
        o1_preview_model,
        o1_mini_model,
    ]

    for model in models:
        model.key = OPENAI_API_KEY

    return models


def build_openai_latest_and_fastest():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    gpt_4o_latest: llm.Model = llm.get_model("gpt-4o")
    gpt_4o_latest.key = OPENAI_API_KEY

    gpt_4o_mini_model: llm.Model = llm.get_model("gpt-4o-mini")
    gpt_4o_mini_model.key = OPENAI_API_KEY

    return gpt_4o_latest, gpt_4o_mini_model


def build_o1_series():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    o1_mini_model: llm.Model = llm.get_model("o1-mini")
    o1_mini_model.key = OPENAI_API_KEY

    o1_preview_model: llm.Model = llm.get_model("o1-preview")
    o1_preview_model.key = OPENAI_API_KEY

    return o1_mini_model, o1_preview_model


def build_small_cheap_and_fast():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    gpt4_o_mini_model: llm.Model = llm.get_model("gpt-4o-mini")
    gpt4_o_mini_model.key = OPENAI_API_KEY

    gemini_1_5_flash_002: llm.Model = llm.get_model("gemini-1.5-flash-002")
    gemini_1_5_flash_002.key = GEMINI_API_KEY

    return gpt4_o_mini_model, gemini_1_5_flash_002


def build_small_cheap_and_fast():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    gpt4_o_mini_model: llm.Model = llm.get_model("gpt-4o-mini")
    gpt4_o_mini_model.key = OPENAI_API_KEY

    gemini_1_5_flash_002: llm.Model = llm.get_model("gemini-1.5-flash-002")
    gemini_1_5_flash_002.key = GEMINI_API_KEY

    return gpt4_o_mini_model, gemini_1_5_flash_002


def build_gemini_1_2_002():
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    gemini_1_5_pro_002: llm.Model = llm.get_model("gemini-1.5-pro-002")
    gemini_1_5_flash_002: llm.Model = llm.get_model("gemini-1.5-flash-002")

    gemini_1_5_pro_002.key = GEMINI_API_KEY
    gemini_1_5_flash_002.key = GEMINI_API_KEY

    return gemini_1_5_pro_002, gemini_1_5_flash_002
