import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.decision import Decision
from app.schemas.decision_schema import DecisionCreate, DecisionResponse
from app.services.embedding_service import generate_embedding, classify_decision

router = APIRouter(prefix="/decisions", tags=["decisions"])


@router.post("/", response_model=DecisionResponse, status_code=201)
async def create_decision(payload: DecisionCreate, db: Session = Depends(get_db)):
    """
    Memory Layer – Capture a new decision:
    1. Auto-classify into category
    2. Generate embedding via sentence-transformers
    3. Store in decisions table with vector
    """
    category_tag = classify_decision(payload.title, payload.reasoning or "")
    embed_text = f"{payload.title} {payload.reasoning or ''} {payload.expected_outcome or ''}"
    embedding = generate_embedding(embed_text)

    decision = Decision(
        id=str(uuid.uuid4()),
        user_id=payload.user_id or "default_user",
        title=payload.title,
        reasoning=payload.reasoning,
        assumptions=payload.assumptions,
        expected_outcome=payload.expected_outcome,
        confidence_score=payload.confidence_score,
        category_tag=category_tag,
        embedding=embedding,
        created_at=datetime.utcnow(),
    )
    db.add(decision)
    db.commit()
    db.refresh(decision)

    return DecisionResponse(
        id=decision.id,
        title=decision.title,
        reasoning=decision.reasoning,
        assumptions=decision.assumptions,
        expected_outcome=decision.expected_outcome,
        confidence_score=decision.confidence_score,
        category_tag=decision.category_tag,
        created_at=decision.created_at.isoformat() if decision.created_at else None,
        user_id=decision.user_id,
    )


@router.get("/", response_model=List[DecisionResponse])
def list_decisions(user_id: str = "default_user", db: Session = Depends(get_db)):
    rows = (
        db.query(Decision)
        .filter(Decision.user_id == user_id)
        .order_by(Decision.created_at.desc())
        .all()
    )
    return [
        DecisionResponse(
            id=d.id, title=d.title, reasoning=d.reasoning,
            assumptions=d.assumptions, expected_outcome=d.expected_outcome,
            confidence_score=d.confidence_score, category_tag=d.category_tag,
            created_at=d.created_at.isoformat() if d.created_at else None,
            user_id=d.user_id,
        )
        for d in rows
    ]


@router.get("/{decision_id}", response_model=DecisionResponse)
def get_decision(decision_id: str, db: Session = Depends(get_db)):
    d = db.query(Decision).filter(Decision.id == decision_id).first()
    if not d:
        raise HTTPException(404, "Decision not found")
    return DecisionResponse(
        id=d.id, title=d.title, reasoning=d.reasoning,
        assumptions=d.assumptions, expected_outcome=d.expected_outcome,
        confidence_score=d.confidence_score, category_tag=d.category_tag,
        created_at=d.created_at.isoformat() if d.created_at else None,
        user_id=d.user_id,
    )
