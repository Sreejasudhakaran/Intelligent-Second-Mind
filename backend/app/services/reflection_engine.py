from typing import Any, Dict, List
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


# ── Principle Extraction Engine ───────────────────────────────────────────────

_PRINCIPLE_PREFIXES = [
    "Always",
    "Never",
    "Before",
    "When",
    "Avoid",
    "Ensure",
    "Prioritize",
    "Do not",
    "Only commit",
    "Allocate",
]

_PRINCIPLE_TEMPLATES = [
    ("price|negotiat|discount|scope", "Do not reduce price under negotiation pressure without adjusting the scope of work."),
    ("delegat|outsourc|hire|va|virtual", "Prepare documented workflows and clear deliverables before delegating any task."),
    ("growth|maintenance|busy|reactive|client", "Allocate a minimum of 30% of weekly effort toward growth activities, not just client maintenance."),
    ("launch|release|deploy|ship|publish", "Validate with one real customer before investing in a full build or launch."),
    ("strategy|plan|pivot|decide|direction", "Write down the downside scenario before committing to any strategic shift."),
    ("market|brand|content|audience|social", "Consistency beats volume — maintain one channel deeply before expanding to new ones."),
    ("revenue|sales|deal|client|contract", "Pursue high-margin opportunities first; low-margin volume creates overhead without compounding value."),
    ("time|schedule|calendar|meeting|call", "Protect focused work blocks from reactive interruptions — schedule meetings in batches."),
    ("assumption|risk|uncertain|unknown", "Surface key assumptions before execution; untested assumptions are the root of most decision failures."),
    ("repeat|same|again|pattern|cycle", "When the same problem recurs, root-cause it before solving it again — patterns signal systemic gaps."),
]


def _derive_principle(lessons_combined: str) -> str:
    """
    Derive a single actionable principle from combined lessons text
    using keyword pattern matching and templates.
    """
    import re
    lower = lessons_combined.lower()
    for pattern, principle in _PRINCIPLE_TEMPLATES:
        if re.search(pattern, lower):
            return principle
    # Generic extraction: take the first meaningful sentence from lessons
    sentences = [s.strip() for s in lessons_combined.replace("\n", ". ").split(".") if len(s.strip()) > 30]
    if sentences:
        s = sentences[0]
        # Normalize to a principle framing
        for prefix in _PRINCIPLE_PREFIXES:
            if s.lower().startswith(prefix.lower()):
                return s if s.endswith(".") else s + "."
        return f"Prioritize: {s}."
    return ""


def extract_principles_from_lessons(lessons_list: List[str]) -> List[str]:
    """
    Given a list of lesson strings (from reflections), extract up to 5 unique
    actionable principles using keyword templates + heuristic derivation.
    
    Called after a user exceeds 5 total reflections.
    """
    if not lessons_list:
        return []

    import re

    # Group lessons by thematic pattern (de-duplicate similar ones)
    seen_patterns: set = set()
    principles: List[str] = []

    for pattern, principle in _PRINCIPLE_TEMPLATES:
        if len(principles) >= 5:
            break
        combined = " ".join(lessons_list).lower()
        if re.search(pattern, combined) and principle not in principles:
            # Check if any lesson actually matches this pattern specifically
            matching = [l for l in lessons_list if re.search(pattern, l.lower())]
            if matching and principle not in principles:
                principles.append(principle)
                seen_patterns.add(pattern)

    # If we haven't filled 5 yet, try deriving from individual lessons
    if len(principles) < 5:
        for lesson in lessons_list:
            if len(principles) >= 5:
                break
            derived = _derive_principle(lesson)
            if derived and derived not in principles and len(derived) > 30:
                principles.append(derived)

    return principles[:5]
