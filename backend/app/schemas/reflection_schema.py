from pydantic import BaseModel, field_validator
from typing import Optional


class ReflectionCreate(BaseModel):
    decision_id: str
    actual_outcome: str
    lessons: Optional[str] = None
    accuracy_score: Optional[int] = None
    user_id: Optional[str] = "default_user"


class ReflectionResponse(BaseModel):
    id: str
    decision_id: str
    actual_outcome: str
    lessons: Optional[str] = None
    accuracy_score: Optional[int] = None
    ai_insight: Optional[str] = None
    created_at: str

    @field_validator("id", "decision_id", mode="before")
    @classmethod
    def coerce_uuid(cls, v):
        return str(v)

    model_config = {"from_attributes": True}
