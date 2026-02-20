from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
import uuid

from database import get_db, settings
from models import WeeklySummary, Insight
from services.llm_service import generate_weekly_insight
from utils.helpers import format_datetime

router = APIRouter(prefix="/insights", tags=["insights"])


class WeeklySummaryCreate(BaseModel):
    user_id: Optional[str] = "default_user"
    week_start: Optional[str] = None
    maintenance_pct: float = 61.0
    growth_pct: float = 19.0
    brand_pct: float = 8.0
    admin_pct: float = 12.0
    strategic_pct: float = 0.0


@router.get("/weekly")
async def get_weekly_insights(
    user_id: str = "default_user",
    db: Session = Depends(get_db),
):
    """Get the latest weekly activity breakdown and AI-generated insight."""
    summary = (
        db.query(WeeklySummary)
        .filter(WeeklySummary.user_id == user_id)
        .order_by(WeeklySummary.week_start.desc())
        .first()
    )

    if not summary:
        # Return demo data if none exists
        demo = {
            "maintenance_pct": 61.0,
            "growth_pct": 19.0,
            "brand_pct": 8.0,
            "admin_pct": 12.0,
            "strategic_pct": 0.0,
        }
        insight_text = await generate_weekly_insight(demo)
        return {
            "summary": demo,
            "ai_insight": insight_text,
            "recent_insights": [],
        }

    summary_dict = {
        "week_start": str(summary.week_start),
        "maintenance_pct": summary.maintenance_pct,
        "growth_pct": summary.growth_pct,
        "brand_pct": summary.brand_pct,
        "admin_pct": summary.admin_pct,
        "strategic_pct": summary.strategic_pct,
    }

    insight_text = await generate_weekly_insight(summary_dict)

    # Store insight
    new_insight = Insight(
        id=str(uuid.uuid4()),
        user_id=user_id,
        insight_type="weekly_pattern",
        description=insight_text,
        created_at=datetime.utcnow(),
    )
    db.add(new_insight)
    db.commit()

    # Get recent insights
    recent = (
        db.query(Insight)
        .filter(Insight.user_id == user_id)
        .order_by(Insight.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "summary": summary_dict,
        "ai_insight": insight_text,
        "recent_insights": [
            {
                "id": i.id,
                "type": i.insight_type,
                "description": i.description,
                "created_at": format_datetime(i.created_at),
            }
            for i in recent
        ],
    }


@router.post("/weekly")
async def create_weekly_summary(
    payload: WeeklySummaryCreate, db: Session = Depends(get_db)
):
    """Create or update the weekly activity summary."""
    week_start = (
        datetime.strptime(payload.week_start, "%Y-%m-%d")
        if payload.week_start
        else datetime.utcnow()
    )

    summary = WeeklySummary(
        id=str(uuid.uuid4()),
        user_id=payload.user_id,
        week_start=week_start,
        maintenance_pct=payload.maintenance_pct,
        growth_pct=payload.growth_pct,
        brand_pct=payload.brand_pct,
        admin_pct=payload.admin_pct,
        strategic_pct=payload.strategic_pct,
    )
    db.add(summary)
    db.commit()
    return {"message": "Weekly summary saved", "id": summary.id}
