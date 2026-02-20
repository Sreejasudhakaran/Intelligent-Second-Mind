from typing import Any, Dict
from app.services.llm_service import generate_reflection_insight


async def run_reflection_engine(
    decision: Dict[str, Any],
    actual_outcome: str,
    lessons: str,
) -> str:
    """
    Reflection Engine:
    1. Takes a past decision + actual outcome + lessons
    2. Calls LLM to compare expected vs actual
    3. Returns AI coaching insight
    """
    return await generate_reflection_insight(decision, actual_outcome, lessons)


def calculate_accuracy_score(expected: str, actual: str) -> int:
    """
    Heuristic accuracy score based on keyword overlap between
    expected and actual outcome texts.
    Returns a score between 0 and 100.
    """
    if not expected or not actual:
        return 50

    expected_words = set(expected.lower().split())
    actual_words = set(actual.lower().split())

    if not expected_words:
        return 50

    overlap = len(expected_words & actual_words)
    score = min(100, int((overlap / len(expected_words)) * 150))
    return max(0, score)
