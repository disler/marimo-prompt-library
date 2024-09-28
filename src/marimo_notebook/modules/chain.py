import json
import re
from typing import List, Dict, Callable, Any, Tuple, Union
from .typings import FusionChainResult
import concurrent.futures


class FusionChain:

    @staticmethod
    def run(
        context: Dict[str, Any],
        models: List[Any],
        callable: Callable,
        prompts: List[str],
        evaluator: Callable[[List[Any]], Tuple[Any, List[float]]],
        get_model_name: Callable[[Any], str],
    ) -> FusionChainResult:
        """
        Run a competition between models on a list of prompts.

        Runs the MinimalChainable.run method for each model for each prompt and evaluates the results.

        The evaluator runs on the last output of each model at the end of the chain of prompts.

        The eval method returns a performance score for each model from 0 to 1, giving priority to models earlier in the list.

        Args:
            context (Dict[str, Any]): The context for the prompts.
            models (List[Any]): List of models to compete.
            callable (Callable): The function to call for each prompt.
            prompts (List[str]): List of prompts to process.
            evaluator (Callable[[List[str]], Tuple[Any, List[float]]]): Function to evaluate model outputs, returning the top response and the scores.
            get_model_name (Callable[[Any], str]): Function to get the name of a model. Defaults to str(model).

        Returns:
            FusionChainResult: A FusionChainResult object containing the top response, all outputs, all context-filled prompts, performance scores, and model names.
        """
        all_outputs = []
        all_context_filled_prompts = []

        for model in models:
            outputs, context_filled_prompts = MinimalChainable.run(
                context, model, callable, prompts
            )
            all_outputs.append(outputs)
            all_context_filled_prompts.append(context_filled_prompts)

        # Evaluate the last output of each model
        last_outputs = [outputs[-1] for outputs in all_outputs]
        top_response, performance_scores = evaluator(last_outputs)

        model_names = [get_model_name(model) for model in models]

        return FusionChainResult(
            top_response=top_response,
            all_prompt_responses=all_outputs,
            all_context_filled_prompts=all_context_filled_prompts,
            performance_scores=performance_scores,
            llm_model_names=model_names,
        )

    @staticmethod
    def run_parallel(
        context: Dict[str, Any],
        models: List[Any],
        callable: Callable,
        prompts: List[str],
        evaluator: Callable[[List[Any]], Tuple[Any, List[float]]],
        get_model_name: Callable[[Any], str],
        num_workers: int = 4,
    ) -> FusionChainResult:
        """
        Run a competition between models on a list of prompts in parallel.

        This method is similar to the 'run' method but utilizes parallel processing
        to improve performance when dealing with multiple models.

        Args:
            context (Dict[str, Any]): The context for the prompts.
            models (List[Any]): List of models to compete.
            callable (Callable): The function to call for each prompt.
            prompts (List[str]): List of prompts to process.
            evaluator (Callable[[List[str]], Tuple[Any, List[float]]]): Function to evaluate model outputs, returning the top response and the scores.
            num_workers (int): Number of parallel workers to use. Defaults to 4.
            get_model_name (Callable[[Any], str]): Function to get the name of a model. Defaults to str(model).

        Returns:
            FusionChainResult: A FusionChainResult object containing the top response, all outputs, all context-filled prompts, performance scores, and model names.
        """

        def process_model(model):
            outputs, context_filled_prompts = MinimalChainable.run(
                context, model, callable, prompts
            )
            return outputs, context_filled_prompts

        all_outputs = []
        all_context_filled_prompts = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            future_to_model = {
                executor.submit(process_model, model): model for model in models
            }
            for future in concurrent.futures.as_completed(future_to_model):
                outputs, context_filled_prompts = future.result()
                all_outputs.append(outputs)
                all_context_filled_prompts.append(context_filled_prompts)

        # Evaluate the last output of each model
        last_outputs = [outputs[-1] for outputs in all_outputs]
        top_response, performance_scores = evaluator(last_outputs)

        model_names = [get_model_name(model) for model in models]

        return FusionChainResult(
            top_response=top_response,
            all_prompt_responses=all_outputs,
            all_context_filled_prompts=all_context_filled_prompts,
            performance_scores=performance_scores,
            llm_model_names=model_names,
        )


class MinimalChainable:
    """
    Sequential prompt chaining with context and output back-references.
    """

    @staticmethod
    def run(
        context: Dict[str, Any], model: Any, callable: Callable, prompts: List[str]
    ) -> Tuple[List[Any], List[str]]:
        # Initialize an empty list to store the outputs
        output = []
        context_filled_prompts = []

        # Iterate over each prompt with its index
        for i, prompt in enumerate(prompts):
            # Iterate over each key-value pair in the context
            for key, value in context.items():
                # Check if the key is in the prompt
                if "{{" + key + "}}" in prompt:
                    # Replace the key with its value
                    prompt = prompt.replace("{{" + key + "}}", str(value))

            # Replace references to previous outputs
            # Iterate from the current index down to 1
            for j in range(i, 0, -1):
                # Get the previous output
                previous_output = output[i - j]

                # Handle JSON (dict) output references
                # Check if the previous output is a dictionary
                if isinstance(previous_output, dict):
                    # Check if the reference is in the prompt
                    if f"{{{{output[-{j}]}}}}" in prompt:
                        # Replace the reference with the JSON string
                        prompt = prompt.replace(
                            f"{{{{output[-{j}]}}}}", json.dumps(previous_output)
                        )
                    # Iterate over each key-value pair in the previous output
                    for key, value in previous_output.items():
                        # Check if the key reference is in the prompt
                        if f"{{{{output[-{j}].{key}}}}}" in prompt:
                            # Replace the key reference with its value
                            prompt = prompt.replace(
                                f"{{{{output[-{j}].{key}}}}}", str(value)
                            )
                # If not a dict, use the original string
                else:
                    # Check if the reference is in the prompt
                    if f"{{{{output[-{j}]}}}}" in prompt:
                        # Replace the reference with the previous output
                        prompt = prompt.replace(
                            f"{{{{output[-{j}]}}}}", str(previous_output)
                        )

            # Append the context filled prompt to the list
            context_filled_prompts.append(prompt)

            # Call the provided callable with the processed prompt
            # Get the result by calling the callable with the model and prompt
            result = callable(model, prompt)

            print("result", result)

            # Try to parse the result as JSON, handling markdown-wrapped JSON
            try:
                # First, attempt to extract JSON from markdown code blocks
                # Search for JSON in markdown code blocks
                json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", result)
                # If a match is found
                if json_match:
                    # Parse the JSON from the match
                    result = json.loads(json_match.group(1))
                else:
                    # If no markdown block found, try parsing the entire result
                    # Parse the entire result as JSON
                    result = json.loads(result)
            except json.JSONDecodeError:
                # Not JSON, keep as is
                pass

            # Append the result to the output list
            output.append(result)

        # Return the list of outputs
        return output, context_filled_prompts

    @staticmethod
    def to_delim_text_file(name: str, content: List[Union[str, dict, list]]) -> str:
        result_string = ""
        with open(f"{name}.txt", "w") as outfile:
            for i, item in enumerate(content, 1):
                if isinstance(item, (dict, list)):
                    item = json.dumps(item)
                elif not isinstance(item, str):
                    item = str(item)
                chain_text_delim = (
                    f"{'🔗' * i} -------- Prompt Chain Result #{i} -------------\n\n"
                )
                outfile.write(chain_text_delim)
                outfile.write(item)
                outfile.write("\n\n")

                result_string += chain_text_delim + item + "\n\n"

        return result_string
