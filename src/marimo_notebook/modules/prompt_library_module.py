import os
import json
from datetime import datetime
from typing import List
from dotenv import load_dotenv
from src.marimo_notebook.modules.typings import ModelRanking, MultiLLMPromptExecution

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
    prompt_library_dir = os.getenv("PROMPT_LIBRARY_DIR", "./prompt_library")
    return pull_in_dir_recursively(prompt_library_dir)


def pull_in_testable_prompts():
    testable_prompts_dir = os.getenv("TESTABLE_PROMPTS_DIR", "./testable_prompts")
    return pull_in_dir_recursively(testable_prompts_dir)


def record_llm_execution(
    prompt: str, list_model_execution_dict: list, prompt_template: str = None
):
    execution_dir = os.getenv("PROMPT_EXECUTIONS_DIR", "./prompt_executions")
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


def pull_in_language_model_rankings():
    rankings_dir = os.getenv("LANGUAGE_MODEL_RANKINGS_DIR", "./language_model_rankings")
    ranking_files = pull_in_dir_recursively(rankings_dir)

    if len(ranking_files) == 0:
        return {}

    return ranking_files


def upsert_rankings_file(name: str, rankings: List[ModelRanking]):
    """
    Upserts a file in the rankings directory. If the file does not exist, it will be created.
    If the file exists, it will be updated.

    rankings: [{
        "llm_model_id": str,
        "score": int,
    }]
    """

    rankings_dir = os.getenv("LANGUAGE_MODEL_RANKINGS_DIR", "./language_model_rankings")
    os.makedirs(rankings_dir, exist_ok=True)

    filename = f"{name}.json"
    filepath = os.path.join(rankings_dir, filename)

    rankings_dict = [ranking.model_dump() for ranking in rankings]
    with open(filepath, "w") as f:
        json.dump(rankings_dict, f, indent=2)


def new_rankings_file(model_ids: List[str]) -> List[ModelRanking]:
    return [ModelRanking(llm_model_id=model_id, score=0) for model_id in model_ids]
