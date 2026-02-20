from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.db import get_db
from app.services.rag_service import find_similar_decisions
from app.services.llm_service import generate_replay_summary, generate_alternative_strategy
from app.models.decision import Decision

router = APIRouter(prefix="/replay", tags=["replay"])


class ReplayRequest(BaseModel):
    query: str
    user_id: Optional[str] = "default_user"
    top_k: Optional[int] = 5


@router.post("/similar")
async def replay_similar(payload: ReplayRequest, db: Session = Depends(get_db)):
    """
    Recall Layer – Semantic similarity search via pgvector:
    1. Embed the user query
    2. Find top-k similar past decisions using cosine similarity
    3. Generate pattern observation summary via LLM
    """
    similar = find_similar_decisions(db, payload.query, payload.user_id, payload.top_k)  # type: ignore
    summary = ""
    if similar:
        summary = await generate_replay_summary(similar, payload.query)
    return {
        "query": payload.query,
        "decisions": similar,
        "pattern_summary": summary,
        "total_found": len(similar),
    }


@router.post("/alternative")
async def alternative_strategy(
    decision_id: str = Query(...),
    db: Session = Depends(get_db),
):
    """
    Alternative Strategy Simulation – Given a past decision,
    use LLM to generate a different strategic approach.
    """
    d = db.query(Decision).filter(Decision.id == decision_id).first()
    if not d:
        from fastapi import HTTPException
        raise HTTPException(404, "Decision not found")

    alt = await generate_alternative_strategy({
        "title": d.title,
        "reasoning": d.reasoning,
        "expected_outcome": d.expected_outcome,
    })
    return {"decision_id": decision_id, "alternative_strategy": alt}
