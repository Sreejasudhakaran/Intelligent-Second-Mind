from typing import List, Dict, Any
from collections import Counter
from app.constants.categories import CATEGORIES


def analyze_weekly_activity(decisions: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Weekly Busy vs Growth Analyzer:
    Given a list of decisions for the past week, calculate
    the percentage breakdown per category.

    Categories:
    - Maintenance → "busy" / reactive
    - Revenue Growth + Strategy → "growth" / proactive
    - Brand, Admin → supporting
    """
    if not decisions:
        return {
            "maintenance_pct": 0.0,
            "growth_pct": 0.0,
            "brand_pct": 0.0,
            "admin_pct": 0.0,
            "strategic_pct": 0.0,
        }

    total = len(decisions)
    counts = Counter(d.get("category_tag", "Strategy") for d in decisions)

    def pct(key: str) -> float:
        return round((counts.get(key, 0) / total) * 100, 1)

    return {
        "maintenance_pct": pct("Maintenance"),
        "growth_pct": pct("Revenue Growth"),
        "brand_pct": pct("Brand"),
        "admin_pct": pct("Admin"),
        "strategic_pct": pct("Strategy"),
    }


def generate_balance_label(summary: Dict[str, float]) -> str:
    """Return a human-readable label for the activity balance."""
    maintenance = summary.get("maintenance_pct", 0)
    growth = summary.get("growth_pct", 0) + summary.get("strategic_pct", 0)

    if maintenance > 60:
        ratio = maintenance / max(growth, 1)
        return f"You are spending {ratio:.1f}x more time maintaining than growing."
    elif growth > maintenance:
        return "Great balance — your growth focus is ahead of maintenance this week."
    else:
        return "Your focus is balanced across maintenance and growth activities."


def prune_and_merge_principles(
    db,
    user_id: str = "default_user",
    max_principles: int = 5,
) -> None:
    """
    Weekly principle maintenance:
    - Keep at most `max_principles` active principles per user.
    - Remove the oldest ones if over the limit (oldest = least relevant).
    Called by the weekly scheduler.
    """
    from app.models.insight import Insight
    from sqlalchemy import asc

    all_principles = (
        db.query(Insight)
        .filter(Insight.user_id == user_id, Insight.insight_type == "principle")
        .order_by(asc(Insight.created_at))
        .all()
    )

    if len(all_principles) <= max_principles:
        return  # Nothing to prune

    # Remove oldest until we're at max
    to_remove = all_principles[:len(all_principles) - max_principles]
    for principle in to_remove:
        db.delete(principle)
    db.commit()
