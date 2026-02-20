from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from services.rag_service import find_similar_decisions, get_latest_weekly_summary
from services.llm_service import generate_daily_guidance

router = APIRouter(prefix="/daily", tags=["daily"])


class DailyGuidanceRequest(BaseModel):
    query: str
    user_id: Optional[str] = "default_user"


@router.post("/guidance")
async def get_daily_guidance(payload: DailyGuidanceRequest, db: Session = Depends(get_db)):
    """
    RAG-powered daily guidance:
    1. Embed the user's query
    2. Retrieve similar past decisions
    3. Fetch latest weekly summary
    4. Generate 3-part strategic guidance
    """
    # Step 1 + 2: RAG retrieval
    similar_decisions = find_similar_decisions(db, payload.query, payload.user_id, top_k=5)

    # Step 3: Weekly context
    weekly_summary = get_latest_weekly_summary(db, payload.user_id)

    # Step 4: LLM guidance generation
    guidance = await generate_daily_guidance(
        payload.query, similar_decisions, weekly_summary
    )

    return {
        "query": payload.query,
        "guidance": guidance,
        "context": {
            "similar_decisions_used": len(similar_decisions),
            "weekly_summary_available": weekly_summary is not None,
        },
    }
