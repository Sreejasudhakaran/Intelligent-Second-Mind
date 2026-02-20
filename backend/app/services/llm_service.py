import logging
from typing import Any, Dict, List
from app.utils.prompts import (
    build_reflection_prompt,
    build_replay_prompt,
    build_daily_guidance_prompt,
    build_insight_prompt,
    build_alternative_strategy_prompt,
)
from app.utils.insight_engine import (
    generate_reflection_insight_rule_based,
    generate_daily_guidance_rule_based,
    generate_weekly_insight_rule_based,
    generate_replay_summary_rule_based,
    generate_alternative_strategy_rule_based,
)

logger = logging.getLogger("jarvis.llm")

# ── Lazy-loaded local pipeline ────────────────────────────────────────────────
_pipe = None


def _get_pipeline():
    global _pipe
    if _pipe is None:
        from transformers import pipeline
        logger.info("Loading local LLM pipeline (flan-t5-base)…")
        _pipe = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            device=-1,
        )
        logger.info("✅ Local LLM pipeline ready")
    return _pipe


def _call_local(prompt: str, max_tokens: int = 256) -> str:
    """Run inference locally. Returns empty string if output quality is too low."""
    # Phrases that indicate the model is echoing the prompt instead of answering it
    _ECHO_PHRASES = [
        "whether the prediction",
        "concrete takeaway",
        "reasoning error",
        "1. whether",
        "2. what reasoning",
        "3. one concrete",
        "be direct, empathetic",
        "in 2-3 sentences",
        "respond with exactly",
        "line 1:", "line 2:", "line 3:",
    ]
    try:
        pipe = _get_pipeline()
        result = pipe(
            prompt,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=0.7,
        )
        text = result[0].get("generated_text", "").strip()
        lower = text.lower()

        # Reject if too short or echoes the prompt structure
        if len(text) < 80:
            return ""
        if any(phrase in lower for phrase in _ECHO_PHRASES):
            logger.warning("LLM output rejected — echoing prompt template. Using rule-based engine.")
            return ""
        return text
    except Exception as e:
        logger.warning(f"Local LLM inference failed: {e}")
        return ""


# ── Public API ────────────────────────────────────────────────────────────────

async def generate_reflection_insight(
    decision: Dict[str, Any], actual_outcome: str, lessons: str
) -> str:
    # Try local model first; fall back to rule-based engine (always high quality)
    result = _call_local(build_reflection_prompt(decision, actual_outcome, lessons), 300)
    if result:
        return result
    return generate_reflection_insight_rule_based(decision, actual_outcome, lessons)


async def generate_replay_summary(decisions: List[Dict], query: str) -> str:
    result = _call_local(build_replay_prompt(decisions, query), 400)
    if result:
        return result
    return generate_replay_summary_rule_based(decisions, query)


async def generate_alternative_strategy(decision: Dict[str, Any]) -> str:
    result = _call_local(build_alternative_strategy_prompt(decision), 200)
    if result:
        return result
    return generate_alternative_strategy_rule_based(decision)


async def generate_daily_guidance(
    query: str,
    similar_decisions: List[Dict],
    weekly_summary: Dict[str, Any] | None,
) -> Dict[str, str]:
    raw = _call_local(build_daily_guidance_prompt(query, similar_decisions, weekly_summary), 512)
    if raw:
        lines = [line.strip() for line in raw.strip().split("\n") if line.strip()]
        if len(lines) >= 3:
            return {
                "high_impact":         lines[0],
                "avoid_busy_work":     lines[1],
                "long_term_alignment": lines[2],
            }
    return generate_daily_guidance_rule_based(query, similar_decisions, weekly_summary)


async def generate_weekly_insight(summary: Dict[str, Any]) -> str:
    result = _call_local(build_insight_prompt(summary), 200)
    if result:
        return result
    return generate_weekly_insight_rule_based(summary)
