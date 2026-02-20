import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.decision import Decision
from app.models.reflection import Reflection
from app.models.insight import Insight
from app.schemas.reflection_schema import ReflectionCreate, ReflectionResponse
from app.services.reflection_engine import (
    run_reflection_engine,
    calculate_accuracy_score,
    extract_principles_from_lessons,
)

router = APIRouter(prefix="/reflections", tags=["reflections"])


@router.post("/", response_model=ReflectionResponse, status_code=201)
async def create_reflection(payload: ReflectionCreate, db: Session = Depends(get_db)):
    """
    Learning Layer – Submit reflection on a past decision:
    1. Retrieve the original decision
    2. Run reflection engine (LLM comparison expected vs actual)
    3. Calculate heuristic accuracy score
    4. Store reflection
    """
    decision = db.query(Decision).filter(Decision.id == payload.decision_id).first()
    if not decision:
        raise HTTPException(404, "Decision not found")

    decision_dict = {
        "title": decision.title,
        "reasoning": decision.reasoning,
        "assumptions": decision.assumptions,
        "expected_outcome": decision.expected_outcome,
        "confidence_score": decision.confidence_score,
    }

    ai_insight = await run_reflection_engine(
        decision_dict, payload.actual_outcome, payload.lessons or ""
    )

    auto_score = calculate_accuracy_score(
        decision.expected_outcome or "", payload.actual_outcome
    )
    score = payload.accuracy_score if payload.accuracy_score is not None else auto_score

    reflection = Reflection(
        id=str(uuid.uuid4()),
        decision_id=payload.decision_id,
        actual_outcome=payload.actual_outcome,
        lessons=payload.lessons,
        accuracy_score=score,
        created_at=datetime.utcnow(),
    )
    db.add(reflection)
    db.commit()
    db.refresh(reflection)

    # ── Principle extraction (triggered when >= 5 reflections exist) ──────────
    # Count total reflections for this user via join on decisions
    total_reflections = (
        db.query(Reflection)
        .join(Decision, Decision.id == Reflection.decision_id)
        .filter(Decision.user_id == (payload.user_id if hasattr(payload, 'user_id') else "default_user"))
        .count()
    )

    if total_reflections >= 5:
        # Fetch last 10 lessons for this user
        all_lessons = (
            db.query(Reflection.lessons)
            .join(Decision, Decision.id == Reflection.decision_id)
            .filter(
                Decision.user_id == (payload.user_id if hasattr(payload, 'user_id') else "default_user"),
                Reflection.lessons != None,
                Reflection.lessons != "",
            )
            .order_by(Reflection.created_at.desc())
            .limit(10)
            .all()
        )
        lessons_list = [r.lessons for r in all_lessons if r.lessons]
        principles = extract_principles_from_lessons(lessons_list)

        # Fetch existing principles to avoid duplicates
        existing = (
            db.query(Insight.description)
            .filter(
                Insight.user_id == (payload.user_id if hasattr(payload, 'user_id') else "default_user"),
                Insight.insight_type == "principle",
            )
            .all()
        )
        existing_texts = {r.description for r in existing}

        for principle_text in principles:
            if principle_text and principle_text not in existing_texts:
                db.add(Insight(
                    id=str(uuid.uuid4()),
                    user_id=(payload.user_id if hasattr(payload, 'user_id') else "default_user"),
                    insight_type="principle",
                    description=principle_text,
                    created_at=datetime.utcnow(),
                ))
                existing_texts.add(principle_text)
        db.commit()

    return ReflectionResponse(
        id=str(reflection.id),
        decision_id=str(reflection.decision_id),
        actual_outcome=reflection.actual_outcome,
        lessons=reflection.lessons,
        accuracy_score=reflection.accuracy_score,
        ai_insight=ai_insight,
        created_at=reflection.created_at.isoformat(),
    )


@router.get("/{decision_id}")
def get_reflection(decision_id: str, db: Session = Depends(get_db)):
    r = db.query(Reflection).filter(Reflection.decision_id == decision_id).first()
    if not r:
        raise HTTPException(404, "No reflection found for this decision")
    return {
        "id": str(r.id),
        "decision_id": str(r.decision_id),
        "actual_outcome": r.actual_outcome,
        "lessons": r.lessons,
        "accuracy_score": r.accuracy_score,
        "created_at": r.created_at.isoformat(),
    }
