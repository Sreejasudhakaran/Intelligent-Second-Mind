import httpx
from typing import Any, Dict, List
from app.config import settings
from app.utils.prompts import (
    build_reflection_prompt,
    build_replay_prompt,
    build_daily_guidance_prompt,
    build_insight_prompt,
    build_alternative_strategy_prompt,
)

HF_URL = "https://api-inference.huggingface.co/models"


async def _call_hf(prompt: str, max_tokens: int = 512) -> str:
    """Internal HuggingFace Inference API caller."""
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.7,
            "return_full_text": False,
        },
    }
    url = f"{HF_URL}/{settings.HUGGINGFACE_MODEL}"
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    if isinstance(data, list) and data:
        return data[0].get("generated_text", "").strip()
    return "Unable to generate a response at this time."


async def generate_reflection_insight(
    decision: Dict[str, Any], actual_outcome: str, lessons: str
) -> str:
    return await _call_hf(build_reflection_prompt(decision, actual_outcome, lessons), 300)


async def generate_replay_summary(decisions: List[Dict], query: str) -> str:
    return await _call_hf(build_replay_prompt(decisions, query), 400)


async def generate_alternative_strategy(decision: Dict[str, Any]) -> str:
    return await _call_hf(build_alternative_strategy_prompt(decision), 200)


async def generate_daily_guidance(
    query: str,
    similar_decisions: List[Dict],
    weekly_summary: Dict[str, Any] | None,
) -> Dict[str, str]:
    prompt = build_daily_guidance_prompt(query, similar_decisions, weekly_summary)
    raw = await _call_hf(prompt, 600)
    lines = [l.strip() for l in raw.strip().split("\n") if l.strip()]
    return {
        "high_impact": lines[0] if len(lines) > 0 else "Focus on your highest-leverage task.",
        "avoid_busy_work": lines[1] if len(lines) > 1 else "Avoid low-value reactive work.",
        "long_term_alignment": lines[2] if len(lines) > 2 else "Keep your long-term vision in focus.",
    }


async def generate_weekly_insight(summary: Dict[str, Any]) -> str:
    return await _call_hf(build_insight_prompt(summary), 200)
