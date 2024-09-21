import os
from dotenv import load_dotenv

load_dotenv()


def pull_in_prompt_library():
    prompt_library_dir = os.getenv("PROMPT_LIBRARY_DIR")
    if not os.path.exists(prompt_library_dir):
        return {}

    prompt_library = {}

    def process_directory(directory):
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, prompt_library_dir)
                with open(file_path, "r") as f:
                    prompt_library[relative_path] = f.read()

    process_directory(prompt_library_dir)

    return prompt_library
