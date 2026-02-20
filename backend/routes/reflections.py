from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

from database import get_db
from models import Decision, Reflection
from services.llm_service import generate_reflection_insight
from utils.helpers import format_datetime

router = APIRouter(prefix="/reflections", tags=["reflections"])


class ReflectionCreate(BaseModel):
    decision_id: str
    actual_outcome: str
    lessons: Optional[str] = None
    accuracy_score: Optional[int] = None


class ReflectionResponse(BaseModel):
    id: str
    decision_id: str
    actual_outcome: str
    lessons: Optional[str]
    accuracy_score: Optional[int]
    ai_insight: Optional[str]
    created_at: str


@router.post("/", response_model=ReflectionResponse)
async def create_reflection(payload: ReflectionCreate, db: Session = Depends(get_db)):
    """Submit a reflection and get AI-generated insight comparing expected vs actual."""
    decision = db.query(Decision).filter(Decision.id == payload.decision_id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")

    decision_dict = {
        "title": decision.title,
        "reasoning": decision.reasoning,
        "assumptions": decision.assumptions,
        "expected_outcome": decision.expected_outcome,
        "confidence_score": decision.confidence_score,
    }

    # Generate LLM insight
    ai_insight = await generate_reflection_insight(
        decision_dict, payload.actual_outcome, payload.lessons or ""
    )

    reflection = Reflection(
        id=str(uuid.uuid4()),
        decision_id=payload.decision_id,
        actual_outcome=payload.actual_outcome,
        lessons=payload.lessons,
        accuracy_score=payload.accuracy_score,
        created_at=datetime.utcnow(),
    )
    db.add(reflection)
    db.commit()
    db.refresh(reflection)

    return ReflectionResponse(
        id=reflection.id,
        decision_id=reflection.decision_id,
        actual_outcome=reflection.actual_outcome,
        lessons=reflection.lessons,
        accuracy_score=reflection.accuracy_score,
        ai_insight=ai_insight,
        created_at=format_datetime(reflection.created_at),
    )


@router.get("/{decision_id}")
def get_reflection_for_decision(decision_id: str, db: Session = Depends(get_db)):
    """Get existing reflection for a decision."""
    reflection = (
        db.query(Reflection)
        .filter(Reflection.decision_id == decision_id)
        .first()
    )
    if not reflection:
        raise HTTPException(status_code=404, detail="No reflection found")
    return {
        "id": reflection.id,
        "decision_id": reflection.decision_id,
        "actual_outcome": reflection.actual_outcome,
        "lessons": reflection.lessons,
        "accuracy_score": reflection.accuracy_score,
        "created_at": format_datetime(reflection.created_at),
    }
