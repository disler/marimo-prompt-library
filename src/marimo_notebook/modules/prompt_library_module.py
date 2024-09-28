import os
import json
from datetime import datetime
from dotenv import load_dotenv
from src.marimo_notebook.modules.typings import MultiLLMPromptExecution

load_dotenv()


def pull_in_dir_recursively(dir: str) -> dict:
    if not os.path.exists(dir):
        return {}

    result = {}

    def recursive_read(current_dir):
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isfile(item_path):
                relative_path = os.path.relpath(item_path, dir)
                with open(item_path, "r") as f:
                    result[relative_path] = f.read()
            elif os.path.isdir(item_path):
                recursive_read(item_path)

    recursive_read(dir)
    return result


def pull_in_prompt_library():
    prompt_library_dir = os.getenv("PROMPT_LIBRARY_DIR")
    return pull_in_dir_recursively(prompt_library_dir)


def pull_in_testable_prompts():
    testable_prompts_dir = os.getenv("TESTABLE_PROMPTS_DIR")
    return pull_in_dir_recursively(testable_prompts_dir)


def record_llm_execution(
    prompt: str, list_model_execution_dict: list, prompt_template: str = None
):
    execution_dir = os.getenv("PROMPT_EXECUTIONS_DIR", "prompt_executions")
    os.makedirs(execution_dir, exist_ok=True)

    if prompt_template:
        filename_base = prompt_template.replace(" ", "_").lower()
    else:
        filename_base = prompt[:50].replace(" ", "_").lower()

    # Clean up filename_base to ensure it's alphanumeric only
    filename_base = "".join(
        char for char in filename_base if char.isalnum() or char == "_"
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_base}_{timestamp}.json"
    filepath = os.path.join(execution_dir, filename)

    execution_record = MultiLLMPromptExecution(
        prompt=prompt,
        prompt_template=prompt_template,
        prompt_responses=list_model_execution_dict,
    )

    with open(filepath, "w") as f:
        json.dump(execution_record.model_dump(), f, indent=2)

    return filepath
