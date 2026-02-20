from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.insight_schema import DailyGuidanceRequest, DailyGuidanceResponse
from app.services.rag_service import find_similar_decisions, get_latest_weekly_summary
from app.services.llm_service import generate_daily_guidance

router = APIRouter(prefix="/daily", tags=["daily"])


@router.post("/guidance", response_model=DailyGuidanceResponse)
async def get_daily_guidance(payload: DailyGuidanceRequest, db: Session = Depends(get_db)):
    """
    Daily Guidance (Cognitive Layer) – Full RAG Pipeline:
    1. Embed user's daily focus query
    2. Retrieve top-5 similar past decisions via pgvector
    3. Fetch latest weekly activity summary
    4. Build context and generate 3-part strategic guidance via LLM
    """
    # Step 1+2: RAG retrieval
    similar_decisions = find_similar_decisions(
        db, payload.query, payload.user_id or "default_user", top_k=5
    )

    # Step 3: Weekly context
    weekly_summary = get_latest_weekly_summary(db, payload.user_id or "default_user")

    # Step 4: LLM generation (with decision_type framing)
    decision_type = getattr(payload, "decision_type", "reversible") or "reversible"
    guidance = await generate_daily_guidance(
        payload.query, similar_decisions, weekly_summary, decision_type
    )

    return DailyGuidanceResponse(
        query=payload.query,
        guidance=guidance,
        context={
            "similar_decisions_used": len(similar_decisions),
            "weekly_summary_available": weekly_summary is not None,
            "top_categories": list({d.get("category_tag") for d in similar_decisions if d.get("category_tag")}),
        },
    )
