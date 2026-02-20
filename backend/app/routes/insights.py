import uuid
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.weekly_summary import WeeklySummary
from app.models.insight import Insight
from app.schemas.insight_schema import WeeklySummaryCreate, WeeklyInsightsResponse
from app.services.llm_service import generate_weekly_insight
from app.services.weekly_analyzer import generate_balance_label

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/weekly", response_model=WeeklyInsightsResponse)
async def get_weekly_insights(user_id: str = "default_user", db: Session = Depends(get_db)):
    """
    Pattern Intelligence Layer:
    1. Fetch latest weekly summary for user
    2. Generate AI insight via LLM
    3. Return breakdown + insight + recent insights
    """
    summary_row = (
        db.query(WeeklySummary)
        .filter(WeeklySummary.user_id == user_id)
        .order_by(WeeklySummary.week_start.desc())
        .first()
    )

    if summary_row:
        summary_dict = {
            "week_start": str(summary_row.week_start),
            "maintenance_pct": summary_row.maintenance_pct,
            "growth_pct": summary_row.growth_pct,
            "brand_pct": summary_row.brand_pct,
            "admin_pct": summary_row.admin_pct,
            "strategic_pct": summary_row.strategic_pct,
        }
    else:
        # Demo data fallback
        summary_dict = {
            "maintenance_pct": 61.0,
            "growth_pct": 19.0,
            "brand_pct": 8.0,
            "admin_pct": 12.0,
            "strategic_pct": 0.0,
        }

    # Generate AI insight
    ai_insight = await generate_weekly_insight(summary_dict)
    balance_label = generate_balance_label(summary_dict)

    # Store insight
    insight_entry = Insight(
        id=str(uuid.uuid4()),
        user_id=user_id,
        insight_type="weekly_pattern",
        description=ai_insight,
        created_at=datetime.utcnow(),
    )
    db.add(insight_entry)
    db.commit()

    # Fetch recent insights
    recent = (
        db.query(Insight)
        .filter(Insight.user_id == user_id)
        .order_by(Insight.created_at.desc())
        .limit(5)
        .all()
    )

    return WeeklyInsightsResponse(
        summary={**summary_dict, "balance_label": balance_label},
        ai_insight=ai_insight,
        recent_insights=[
            {
                "id": str(i.id),
                "type": i.insight_type,
                "description": i.description,
                "created_at": i.created_at.isoformat(),
            }
            for i in recent
        ],
    )


@router.post("/weekly", status_code=201)
async def create_weekly_summary(payload: WeeklySummaryCreate, db: Session = Depends(get_db)):
    """Manually create a weekly activity summary."""
    week_start = (
        datetime.strptime(payload.week_start, "%Y-%m-%d").date()
        if payload.week_start
        else datetime.utcnow().date()
    )
    entry = WeeklySummary(
        id=str(uuid.uuid4()),
        user_id=payload.user_id,
        week_start=week_start,
        maintenance_pct=payload.maintenance_pct,
        growth_pct=payload.growth_pct,
        brand_pct=payload.brand_pct,
        admin_pct=payload.admin_pct,
        strategic_pct=payload.strategic_pct,
    )
    db.add(entry)
    db.commit()
    return {"message": "Weekly summary saved", "id": str(entry.id)}
