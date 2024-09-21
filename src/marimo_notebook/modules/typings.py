from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional, Union, Any


class FusionChainResult(BaseModel):
    top_response: Union[str, Dict[str, Any]]
    all_prompt_responses: List[List[Any]]
    all_context_filled_prompts: List[List[str]]
    performance_scores: List[float]
    model_names: List[str]
