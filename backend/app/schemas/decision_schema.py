from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class DecisionCreate(BaseModel):
    title: str
    reasoning: Optional[str] = None
    assumptions: Optional[str] = None
    expected_outcome: Optional[str] = None
    confidence_score: Optional[int] = 50
    user_id: Optional[str] = "default_user"
    decision_type: Optional[str] = "reversible"  # reversible | irreversible


class DecisionResponse(BaseModel):
    id: str
    title: str
    reasoning: Optional[str] = None
    assumptions: Optional[str] = None
    expected_outcome: Optional[str] = None
    confidence_score: Optional[int] = None
    category_tag: Optional[str] = None
    decision_type: Optional[str] = "reversible"
    created_at: Optional[str] = None
    user_id: str

    @field_validator("id", mode="before")
    @classmethod
    def coerce_id(cls, v):
        return str(v)

    model_config = {"from_attributes": True}


class DecisionWithSimilarity(DecisionResponse):
    similarity: Optional[float] = None
    actual_outcome: Optional[str] = None
    lessons: Optional[str] = None

