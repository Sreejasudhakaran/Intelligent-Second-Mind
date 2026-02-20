from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

from database import get_db
from models import Decision, Reflection
from services.embedding_service import generate_embedding, classify_decision
from services.llm_service import generate_reflection_insight
from utils.helpers import format_datetime

router = APIRouter(prefix="/decisions", tags=["decisions"])


class DecisionCreate(BaseModel):
    title: str
    reasoning: Optional[str] = None
    assumptions: Optional[str] = None
    expected_outcome: Optional[str] = None
    confidence_score: Optional[int] = 50
    user_id: Optional[str] = "default_user"


class DecisionResponse(BaseModel):
    id: str
    title: str
    reasoning: Optional[str]
    assumptions: Optional[str]
    expected_outcome: Optional[str]
    confidence_score: Optional[int]
    category_tag: Optional[str]
    created_at: Optional[str]
    user_id: str

    class Config:
        from_attributes = True


@router.post("/", response_model=DecisionResponse)
async def create_decision(payload: DecisionCreate, db: Session = Depends(get_db)):
    """Capture a new decision with auto-embedding and auto-tagging."""
    # Auto-classify
    category_tag = classify_decision(payload.title, payload.reasoning or "")

    # Generate embedding from combined text
    text_for_embedding = f"{payload.title} {payload.reasoning or ''} {payload.expected_outcome or ''}"
    embedding = generate_embedding(text_for_embedding)

    decision = Decision(
        id=str(uuid.uuid4()),
        user_id=payload.user_id,
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
        created_at=format_datetime(decision.created_at),
        user_id=decision.user_id,
    )


@router.get("/", response_model=List[DecisionResponse])
def get_decisions(user_id: str = "default_user", db: Session = Depends(get_db)):
    """Get all decisions for a user, newest first."""
    decisions = (
        db.query(Decision)
        .filter(Decision.user_id == user_id)
        .order_by(Decision.created_at.desc())
        .all()
    )
    return [
        DecisionResponse(
            id=d.id,
            title=d.title,
            reasoning=d.reasoning,
            assumptions=d.assumptions,
            expected_outcome=d.expected_outcome,
            confidence_score=d.confidence_score,
            category_tag=d.category_tag,
            created_at=format_datetime(d.created_at),
            user_id=d.user_id,
        )
        for d in decisions
    ]


@router.get("/{decision_id}", response_model=DecisionResponse)
def get_decision(decision_id: str, db: Session = Depends(get_db)):
    decision = db.query(Decision).filter(Decision.id == decision_id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return DecisionResponse(
        id=decision.id,
        title=decision.title,
        reasoning=decision.reasoning,
        assumptions=decision.assumptions,
        expected_outcome=decision.expected_outcome,
        confidence_score=decision.confidence_score,
        category_tag=decision.category_tag,
        created_at=format_datetime(decision.created_at),
        user_id=decision.user_id,
    )
