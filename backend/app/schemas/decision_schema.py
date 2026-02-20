from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DecisionCreate(BaseModel):
    title: str
    reasoning: Optional[str] = None
    assumptions: Optional[str] = None
    expected_outcome: Optional[str] = None
    confidence_score: Optional[int] = 50
    user_id: Optional[str] = "default_user"


class DecisionResponse(BaseModel):
    id: str
    title: str
    reasoning: Optional[str] = None
    assumptions: Optional[str] = None
    expected_outcome: Optional[str] = None
    confidence_score: Optional[int] = None
    category_tag: Optional[str] = None
    created_at: Optional[str] = None
    user_id: str

    model_config = {"from_attributes": True}


class DecisionWithSimilarity(DecisionResponse):
    similarity: Optional[float] = None
    actual_outcome: Optional[str] = None
    lessons: Optional[str] = None
