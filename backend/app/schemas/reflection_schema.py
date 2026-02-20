from pydantic import BaseModel
from typing import Optional


class ReflectionCreate(BaseModel):
    decision_id: str
    actual_outcome: str
    lessons: Optional[str] = None
    accuracy_score: Optional[int] = None


class ReflectionResponse(BaseModel):
    id: str
    decision_id: str
    actual_outcome: str
    lessons: Optional[str] = None
    accuracy_score: Optional[int] = None
    ai_insight: Optional[str] = None
    created_at: str

    model_config = {"from_attributes": True}
