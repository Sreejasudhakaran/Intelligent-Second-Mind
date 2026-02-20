from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Decision, Reflection, WeeklySummary
from services.embedding_service import generate_embedding
from typing import List, Dict, Any


def find_similar_decisions(
    db: Session, query: str, user_id: str = "default_user", top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    RAG: Generate embedding for query, find top-k similar decisions
    using pgvector cosine similarity search.
    """
    query_embedding = generate_embedding(query)
    embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

    sql = text("""
        SELECT id, title, reasoning, assumptions, expected_outcome,
               confidence_score, category_tag, created_at,
               1 - (embedding <=> :embedding::vector) AS similarity
        FROM decisions
        WHERE user_id = :user_id
          AND embedding IS NOT NULL
        ORDER BY embedding <=> :embedding::vector
        LIMIT :top_k
    """)

    results = db.execute(
        sql,
        {"embedding": embedding_str, "user_id": user_id, "top_k": top_k},
    ).fetchall()

    decisions = []
    for row in results:
        decision_dict = {
            "id": str(row.id),
            "title": row.title,
            "reasoning": row.reasoning,
            "assumptions": row.assumptions,
            "expected_outcome": row.expected_outcome,
            "confidence_score": row.confidence_score,
            "category_tag": row.category_tag,
            "created_at": str(row.created_at),
            "similarity": float(row.similarity),
        }

        # Attach reflection if available
        reflection = (
            db.query(Reflection)
            .filter(Reflection.decision_id == str(row.id))
            .first()
        )
        if reflection:
            decision_dict["actual_outcome"] = reflection.actual_outcome
            decision_dict["lessons"] = reflection.lessons

        decisions.append(decision_dict)

    return decisions


def get_latest_weekly_summary(
    db: Session, user_id: str = "default_user"
) -> Dict[str, Any] | None:
    """Retrieve the most recent weekly summary for a user."""
    summary = (
        db.query(WeeklySummary)
        .filter(WeeklySummary.user_id == user_id)
        .order_by(WeeklySummary.week_start.desc())
        .first()
    )
    if not summary:
        return None
    return {
        "week_start": str(summary.week_start),
        "maintenance_pct": summary.maintenance_pct,
        "growth_pct": summary.growth_pct,
        "brand_pct": summary.brand_pct,
        "admin_pct": summary.admin_pct,
        "strategic_pct": summary.strategic_pct,
    }


def build_rag_context(
    similar_decisions: List[Dict[str, Any]],
    weekly_summary: Dict[str, Any] | None,
) -> str:
    """Build a structured context string for LLM from RAG results."""
    context_parts = []

    if similar_decisions:
        context_parts.append("## Relevant Past Decisions:")
        for i, d in enumerate(similar_decisions[:5], 1):
            context_parts.append(
                f"{i}. [{d.get('category_tag', 'Unknown')}] {d['title']}\n"
                f"   Reasoning: {d.get('reasoning', 'N/A')}\n"
                f"   Expected: {d.get('expected_outcome', 'N/A')}\n"
                f"   Actual: {d.get('actual_outcome', 'Not yet reflected')}\n"
                f"   Lesson: {d.get('lessons', 'None yet')}"
            )

    if weekly_summary:
        context_parts.append("\n## This Week's Activity Balance:")
        context_parts.append(
            f"   Maintenance: {weekly_summary.get('maintenance_pct', 0):.0f}%\n"
            f"   Revenue Growth: {weekly_summary.get('growth_pct', 0):.0f}%\n"
            f"   Brand: {weekly_summary.get('brand_pct', 0):.0f}%\n"
            f"   Admin: {weekly_summary.get('admin_pct', 0):.0f}%\n"
            f"   Strategy: {weekly_summary.get('strategic_pct', 0):.0f}%"
        )

    return "\n".join(context_parts)
