from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class Observation(BaseModel):
    data: List[Dict[str, Any]]
    step_count: int


class Action(BaseModel):
    action_type: str  # fill_missing, normalize, remove_duplicates
    column: Optional[str] = None


class Reward(BaseModel):
    score: float
