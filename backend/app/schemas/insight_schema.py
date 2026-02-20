from pydantic import BaseModel, field_validator
from typing import Optional, List


class WeeklySummaryCreate(BaseModel):
    user_id: Optional[str] = "default_user"
    week_start: Optional[str] = None
    maintenance_pct: float = 61.0
    growth_pct: float = 19.0
    brand_pct: float = 8.0
    admin_pct: float = 12.0
    strategic_pct: float = 0.0


class InsightResponse(BaseModel):
    id: str
    user_id: str
    insight_type: Optional[str] = None
    description: Optional[str] = None
    created_at: str

    @field_validator("id", "user_id", mode="before")
    @classmethod
    def coerce_uuid(cls, v):
        return str(v)

    model_config = {"from_attributes": True}


class WeeklyInsightsResponse(BaseModel):
    summary: dict
    ai_insight: str
    recent_insights: List[dict] = []


class DailyGuidanceRequest(BaseModel):
    query: str
    user_id: Optional[str] = "default_user"


class DailyGuidanceResponse(BaseModel):
    query: str
    guidance: dict
    context: dict
