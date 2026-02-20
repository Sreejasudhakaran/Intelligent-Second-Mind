from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.services.embedding_service import generate_embedding
from app.models.reflection import Reflection
from app.models.weekly_summary import WeeklySummary


def find_similar_decisions(
    db: Session,
    query: str,
    user_id: str = "default_user",
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    RAG Step 1–2: Embed the query, run pgvector cosine similarity search,
    return top-k decisions enriched with their reflection outcomes.
    """
    # Step 1: Generate embedding
    query_embedding = generate_embedding(query)
    embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

    # Step 2: pgvector cosine similarity query
    sql = text("""
        SELECT id, title, reasoning, assumptions, expected_outcome,
               confidence_score, category_tag, created_at,
               1 - (embedding <=> :emb::vector) AS similarity
        FROM decisions
        WHERE user_id = :uid
          AND embedding IS NOT NULL
        ORDER BY embedding <=> :emb::vector
        LIMIT :k
    """)

    rows = db.execute(sql, {"emb": embedding_str, "uid": user_id, "k": top_k}).fetchall()

    results = []
    for row in rows:
        d = {
            "id": str(row.id),
            "title": row.title,
            "reasoning": row.reasoning,
            "assumptions": row.assumptions,
            "expected_outcome": row.expected_outcome,
            "confidence_score": row.confidence_score,
            "category_tag": row.category_tag,
            "created_at": str(row.created_at),
            "similarity": round(float(row.similarity), 4),
        }
        # Attach reflection if available
        reflection = (
            db.query(Reflection).filter(Reflection.decision_id == str(row.id)).first()
        )
        if reflection:
            d["actual_outcome"] = reflection.actual_outcome
            d["lessons"] = reflection.lessons
        results.append(d)

    return results


def get_latest_weekly_summary(
    db: Session, user_id: str = "default_user"
) -> Dict[str, Any] | None:
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
    """Build a structured context string for the LLM prompt."""
    parts = []

    if similar_decisions:
        parts.append("## Relevant Past Decisions:")
        for i, d in enumerate(similar_decisions[:5], 1):
            parts.append(
                f"{i}. [{d.get('category_tag', 'Unknown')}] {d['title']}\n"
                f"   Expected: {d.get('expected_outcome', 'N/A')}\n"
                f"   Actual: {d.get('actual_outcome', 'Not yet reflected')}\n"
                f"   Lesson: {d.get('lessons', 'None yet')}"
            )

    if weekly_summary:
        parts.append("\n## This Week's Activity Balance:")
        parts.append(
            f"   Maintenance {weekly_summary.get('maintenance_pct', 0):.0f}% | "
            f"Growth {weekly_summary.get('growth_pct', 0):.0f}% | "
            f"Brand {weekly_summary.get('brand_pct', 0):.0f}% | "
            f"Admin {weekly_summary.get('admin_pct', 0):.0f}% | "
            f"Strategy {weekly_summary.get('strategic_pct', 0):.0f}%"
        )

    return "\n".join(parts)
