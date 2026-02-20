from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from services.rag_service import find_similar_decisions
from services.llm_service import generate_replay_summary, generate_alternative_strategy

router = APIRouter(prefix="/replay", tags=["replay"])


class ReplayRequest(BaseModel):
    query: str
    user_id: Optional[str] = "default_user"
    top_k: Optional[int] = 5


@router.post("/similar")
async def replay_similar_decisions(payload: ReplayRequest, db: Session = Depends(get_db)):
    """
    Vector similarity search: find top-k similar past decisions
    and generate a pattern summary.
    """
    similar = find_similar_decisions(db, payload.query, payload.user_id, payload.top_k)
    summary = ""
    if similar:
        summary = await generate_replay_summary(similar, payload.query)

    return {
        "query": payload.query,
        "decisions": similar,
        "pattern_summary": summary,
    }


@router.post("/alternative")
async def generate_alternative(
    decision_id: str = Query(..., description="ID of the decision to simulate alternatives for"),
    db: Session = Depends(get_db),
):
    """Generate an alternative strategy for a given decision using LLM."""
    from models import Decision
    decision = db.query(Decision).filter(Decision.id == decision_id).first()
    if not decision:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Decision not found")

    decision_dict = {
        "title": decision.title,
        "reasoning": decision.reasoning,
        "expected_outcome": decision.expected_outcome,
    }
    alternative = await generate_alternative_strategy(decision_dict)
    return {"decision_id": decision_id, "alternative_strategy": alternative}
