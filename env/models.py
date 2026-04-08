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


def create_action(action_type: str, column: Optional[str] = None) -> Action:
    """Create an Action instance with proper typing."""
    return Action(action_type=action_type, column=column)


def create_observation(data: List[Dict[str, Any]], step_count: int) -> Observation:
    """Create an Observation instance with proper typing."""
    return Observation(data=data, step_count=step_count)
