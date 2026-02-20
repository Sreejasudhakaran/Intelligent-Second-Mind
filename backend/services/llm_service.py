import httpx
from database import settings
from utils.prompts import (
    build_reflection_prompt,
    build_replay_prompt,
    build_daily_guidance_prompt,
    build_insight_prompt,
)
from typing import Any, Dict


HF_API_URL = "https://api-inference.huggingface.co/models"


async def call_hf_model(prompt: str, max_tokens: int = 512) -> str:
    """Call HuggingFace Inference API and return generated text."""
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.7,
            "return_full_text": False,
        },
    }
    url = f"{HF_API_URL}/{settings.HUGGINGFACE_MODEL}"

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    if isinstance(data, list) and len(data) > 0:
        return data[0].get("generated_text", "").strip()
    return "I was unable to generate a response at this time."


async def generate_reflection_insight(
    decision: Dict[str, Any], actual_outcome: str, lessons: str
) -> str:
    prompt = build_reflection_prompt(decision, actual_outcome, lessons)
    return await call_hf_model(prompt, max_tokens=300)


async def generate_replay_summary(decisions: list, query: str) -> str:
    prompt = build_replay_prompt(decisions, query)
    return await call_hf_model(prompt, max_tokens=400)


async def generate_alternative_strategy(decision: Dict[str, Any]) -> str:
    prompt = f"""You are JARVIS, an AI decision intelligence system.
Given this decision:
Title: {decision.get('title')}
Reasoning: {decision.get('reasoning')}
Expected Outcome: {decision.get('expected_outcome')}

Suggest ONE alternative strategic approach the person could have taken instead.
Be concise, specific, and actionable. Answer in 2-3 sentences."""
    return await call_hf_model(prompt, max_tokens=200)


async def generate_daily_guidance(
    query: str,
    similar_decisions: list,
    weekly_summary: Dict[str, Any] | None,
) -> Dict[str, str]:
    prompt = build_daily_guidance_prompt(query, similar_decisions, weekly_summary)
    raw = await call_hf_model(prompt, max_tokens=600)

    # Parse structured output
    lines = [l.strip() for l in raw.strip().split("\n") if l.strip()]
    high_impact = lines[0] if len(lines) > 0 else "Focus on your highest-leverage task today."
    avoid_busy = lines[1] if len(lines) > 1 else "Avoid low-value reactive work."
    long_term = lines[2] if len(lines) > 2 else "Keep your long-term vision in focus."

    return {
        "high_impact": high_impact,
        "avoid_busy_work": avoid_busy,
        "long_term_alignment": long_term,
    }


async def generate_weekly_insight(summary: Dict[str, Any]) -> str:
    prompt = build_insight_prompt(summary)
    return await call_hf_model(prompt, max_tokens=200)
