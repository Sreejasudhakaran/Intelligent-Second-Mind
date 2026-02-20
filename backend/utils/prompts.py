from typing import Any, Dict, List


def build_reflection_prompt(
    decision: Dict[str, Any], actual_outcome: str, lessons: str
) -> str:
    return f"""You are JARVIS, a personal AI decision coach.

A user made this decision:
Title: {decision.get('title')}
Reasoning: {decision.get('reasoning')}
Assumptions: {decision.get('assumptions')}
Expected Outcome: {decision.get('expected_outcome')}
Confidence: {decision.get('confidence_score')}%

Now they are reflecting:
Actual Outcome: {actual_outcome}
What they learned: {lessons}

In 2-3 sentences, give them a thoughtful, honest analysis:
- Was their prediction accurate?
- What can they improve in future decision-making?
- One actionable takeaway.

Be direct, empathetic, and specific."""


def build_replay_prompt(decisions: List[Dict[str, Any]], query: str) -> str:
    decision_text = "\n".join(
        f"- {d['title']} ({d.get('category_tag', 'Unknown')}): "
        f"Expected '{d.get('expected_outcome', 'N/A')}', "
        f"Actual '{d.get('actual_outcome', 'not yet reflected')}'"
        for d in decisions
    )
    return f"""You are JARVIS, an AI decision intelligence system.

The user is searching for decisions related to: "{query}"

Here are the most similar past decisions:
{decision_text}

In 2-3 sentences, summarize:
1. What patterns you notice across these decisions
2. Whether there's a recurring reasoning style or outcome

Be concise, insightful, and personal."""


def build_daily_guidance_prompt(
    query: str,
    similar_decisions: List[Dict[str, Any]],
    weekly_summary: Dict[str, Any] | None,
) -> str:
    decision_context = "\n".join(
        f"- {d['title']}: {d.get('expected_outcome', 'N/A')}"
        for d in similar_decisions[:3]
    )

    weekly_context = ""
    if weekly_summary:
        weekly_context = (
            f"\nThis week: Maintenance {weekly_summary.get('maintenance_pct', 0):.0f}%, "
            f"Growth {weekly_summary.get('growth_pct', 0):.0f}%, "
            f"Brand {weekly_summary.get('brand_pct', 0):.0f}%"
        )

    return f"""You are JARVIS, a calm and intelligent AI decision advisor.

The user asks: "{query}"

Their relevant past decisions:
{decision_context}
{weekly_context}

Respond with EXACTLY 3 lines (one per suggestion), no bullets, no labels:
Line 1: The single highest-impact action they should take today
Line 2: One specific type of busy work they should avoid
Line 3: How today's focus connects to their long-term goals

Be specific, direct, and motivating. No fluff."""


def build_insight_prompt(summary: Dict[str, Any]) -> str:
    maintenance = summary.get("maintenance_pct", 0)
    growth = summary.get("growth_pct", 0)
    ratio = maintenance / growth if growth > 0 else 99

    return f"""You are JARVIS, a strategic AI coach.

This week's activity breakdown:
- Maintenance: {maintenance:.0f}%
- Revenue Growth: {growth:.0f}%
- Brand: {summary.get('brand_pct', 0):.0f}%
- Admin: {summary.get('admin_pct', 0):.0f}%
- Strategy: {summary.get('strategic_pct', 0):.0f}%

The maintenance-to-growth ratio is {ratio:.1f}x.

In ONE sentence, give a sharp, personal insight about what this pattern reveals
about how the user is spending their energy this week. Be honest and specific."""
