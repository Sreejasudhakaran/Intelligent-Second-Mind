import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.models.decision import Decision
from app.models.weekly_summary import WeeklySummary
from app.models.insight import Insight
from app.schemas.insight_schema import WeeklySummaryCreate, WeeklyInsightsResponse
from app.services.llm_service import generate_weekly_insight
from app.services.weekly_analyzer import generate_balance_label

router = APIRouter(prefix="/insights", tags=["insights"])

# Maps decision category_tag values → summary percentage keys
# Must match keys in app/constants/categories.py EXACTLY
CATEGORY_MAP = {
    "Revenue Growth": "growth_pct",
    "Maintenance":    "maintenance_pct",
    "Brand":          "brand_pct",
    "Admin":          "admin_pct",
    "Strategy":       "strategic_pct",
}


PERIOD_DAYS = {
    "week":    7,
    "month":   30,
    "quarter": 90,
    "year":    365,
    "all":     None,
}


def _compute_from_decisions(db: Session, user_id: str, period: str = "week") -> dict:
    """Compute category breakdown percentages filtered by time period."""
    query = (
        db.query(Decision.category_tag, func.count(Decision.id).label("cnt"))
        .filter(Decision.user_id == user_id)
    )
    days = PERIOD_DAYS.get(period)
    if days is not None:
        cutoff = datetime.utcnow() - timedelta(days=days)
        query = query.filter(Decision.created_at >= cutoff)

    rows = query.group_by(Decision.category_tag).all()
    if not rows:
        return None

    total = sum(r.cnt for r in rows)
    counts = {r.category_tag: r.cnt for r in rows}

    summary = {
        "maintenance_pct": 0.0,
        "growth_pct":       0.0,
        "brand_pct":        0.0,
        "admin_pct":        0.0,
        "strategic_pct":    0.0,
        "total_decisions":  total,
    }
    for tag, key in CATEGORY_MAP.items():
        if tag in counts:
            summary[key] = round((counts[tag] / total) * 100, 1)
    for tag, cnt in counts.items():
        if tag not in CATEGORY_MAP:
            summary["maintenance_pct"] += round((cnt / total) * 100, 1)
    return summary


@router.get("/weekly", response_model=WeeklyInsightsResponse)
async def get_weekly_insights(
    user_id: str = "default_user",
    period: str = "week",
    db: Session = Depends(get_db),
):
    """
    Pattern Intelligence: period = week | month | quarter | year | all
    Computes category breakdown live from decisions filtered by time period.
    """
    if period not in PERIOD_DAYS:
        period = "week"

    # ── Primary: compute live from decisions ─────────────────────────────────
    live_summary = _compute_from_decisions(db, user_id, period)

    if live_summary:
        summary_dict = live_summary
        source = "live"
    else:
        # ── Fallback 1: manually entered weekly summary ───────────────────────
        summary_row = (
            db.query(WeeklySummary)
            .filter(WeeklySummary.user_id == user_id)
            .order_by(WeeklySummary.week_start.desc())
            .first()
        )
        if summary_row:
            summary_dict = {
                "week_start":     str(summary_row.week_start),
                "maintenance_pct": summary_row.maintenance_pct,
                "growth_pct":      summary_row.growth_pct,
                "brand_pct":       summary_row.brand_pct,
                "admin_pct":       summary_row.admin_pct,
                "strategic_pct":   summary_row.strategic_pct,
                "total_decisions": 0,
            }
            source = "manual"
        else:
            # ── Fallback 2: empty state ───────────────────────────────────────
            summary_dict = {
                "maintenance_pct": 0.0,
                "growth_pct":      0.0,
                "brand_pct":       0.0,
                "admin_pct":       0.0,
                "strategic_pct":   0.0,
                "total_decisions": 0,
            }
            source = "empty"

    # Generate AI insight
    ai_insight = await generate_weekly_insight(summary_dict)
    balance_label = generate_balance_label(summary_dict)

    # Fetch last 5 unique insights (avoid duplicates by ordering + limiting)
    recent = (
        db.query(Insight)
        .filter(Insight.user_id == user_id)
        .order_by(Insight.created_at.desc())
        .limit(5)
        .all()
    )

    # Only store a new insight if it's meaningfully different from the last one
    should_store = (
        source == "live"
        and ai_insight
        and (not recent or recent[0].description != ai_insight)
    )
    if should_store:
        insight_entry = Insight(
            id=str(uuid.uuid4()),
            user_id=user_id,
            insight_type="weekly_pattern",
            description=ai_insight,
            created_at=datetime.utcnow(),
        )
        db.add(insight_entry)
        db.commit()
        db.refresh(insight_entry)
        recent = [insight_entry] + list(recent[:4])

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
    """Manually override the weekly activity summary."""
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


@router.get("/principles")
def get_principles(user_id: str = "default_user", db: Session = Depends(get_db)):
    """
    Return stored behavioral principles (insight_type='principle') for a user.
    Also returns total reflection count to show context.
    """
    from app.models.reflection import Reflection
    from app.models.decision import Decision

    principles = (
        db.query(Insight)
        .filter(Insight.user_id == user_id, Insight.insight_type == "principle")
        .order_by(Insight.created_at.desc())
        .limit(5)
        .all()
    )

    # Count total reflections for this user
    total_reflections = (
        db.query(Reflection)
        .join(Decision, Decision.id == Reflection.decision_id)
        .filter(Decision.user_id == user_id)
        .count()
    )

    return {
        "principles": [
            {
                "id": str(p.id),
                "description": p.description,
                "created_at": p.created_at.isoformat(),
            }
            for p in principles
        ],
        "total_reflections": total_reflections,
        "extraction_threshold": 5,
    }
