"""
Decision Service — Auto-classification of decision reversibility.

classify_decision_type(decision_text) -> "reversible" | "irreversible"

Strategy:
1. Try local flan-t5 LLM (single token output check)
2. Fall back to fast rule-based keyword classifier
"""

import re
import logging
from app.utils.prompts import build_reversibility_prompt

logger = logging.getLogger("jarvis.decision_service")

# ── Irreversibility keyword rules ─────────────────────────────────────────────
# Ordered by specificity. ANY match → irreversible.
_IRREVERSIBLE_PATTERNS = [
    # Financial lock-in
    r"\b(debt|loan|finance|borrow|invest(ment)?|equity|capital raise|fund(ing)?)\b",
    # Contracts / legal
    r"\b(contract|agreement|sign(ing)?|lease|binding|exclusive|partner(ship)?|joint venture)\b",
    # Hiring / headcount
    r"\b(hire|hiring|employ|full.?time|permanent staff|headcount|recruit)\b",
    # Pricing strategy shifts
    r"\b(increase.{0,20}price|price.{0,20}increase|repric|pricing model|premium pricing)\b",
    # Brand repositioning
    r"\b(rebrand|reposit|brand pivot|brand identity|new brand|brand shift)\b",
    # Market / strategic pivot
    r"\b(pivot|enter.{0,20}market|new market|market entry|strategic shift|exit.{0,20}market)\b",
    # Resource commitment
    r"\b(outsourc|automat|replac|shut down|close|discontinu|exit|divest|sell.{0,20}business)\b",
    # Long-term planning signals
    r"\b(long.?term|multi.?year|5.year|3.year|10.year|permanent|irrevoc)\b",
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in _IRREVERSIBLE_PATTERNS]


def _rule_based_classify(text: str) -> str:
    """Fast keyword-based classifier. Returns 'reversible' or 'irreversible'."""
    for pattern in _COMPILED:
        if pattern.search(text):
            logger.debug(f"Irreversible matched by pattern: {pattern.pattern[:40]}")
            return "irreversible"
    return "reversible"


def _llm_classify(text: str) -> str:
    """
    Try local flan-t5 for classification. Expects a single-word output.
    Returns '' if model output is unusable.
    """
    try:
        from app.services.llm_service import _call_local
        prompt = build_reversibility_prompt(text)
        result = _call_local(prompt, max_tokens=5)
        word = result.strip().lower().split()[0] if result.strip() else ""
        if word in ("reversible", "irreversible"):
            return word
    except Exception as e:
        logger.warning(f"LLM classification failed: {e}")
    return ""


def classify_decision_type(
    title: str = "",
    reasoning: str = "",
    assumptions: str = "",
    expected_outcome: str = "",
) -> str:
    """
    Auto-classify a decision as 'reversible' or 'irreversible'.

    Args:
        title, reasoning, assumptions, expected_outcome — decision context strings

    Returns:
        'reversible' | 'irreversible'
    """
    decision_text = " ".join(filter(None, [title, reasoning, assumptions, expected_outcome]))

    if not decision_text.strip():
        return "reversible"  # Default safe

    # Rule-based first (fast, deterministic, reliable)
    rule_result = _rule_based_classify(decision_text)

    # If rule-based says irreversible → trust it immediately
    if rule_result == "irreversible":
        logger.info(f"Classified as IRREVERSIBLE (rule-based): {title[:50]}")
        return "irreversible"

    # If rule-based says reversible, optionally confirm with LLM
    llm_result = _llm_classify(decision_text)
    if llm_result:
        logger.info(f"Classified as {llm_result.upper()} (LLM): {title[:50]}")
        return llm_result

    logger.info(f"Classified as REVERSIBLE (default): {title[:50]}")
    return "reversible"
