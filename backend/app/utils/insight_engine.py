"""
insight_engine.py
─────────────────
Smart rule-based JARVIS insight generator.
Produces original, analytical responses by reasoning over the provided data —
no LLM required. Used as the primary fallback when local model output is weak.
"""

from typing import Any, Dict, List, Optional
import re


# ── Helpers ───────────────────────────────────────────────────────────────────

def _gap_score(expected: str, actual: str) -> float:
    """Rough semantic distance: 0.0 = perfect match, 1.0 = completely different."""
    if not expected or not actual:
        return 0.5
    exp_words = set(re.findall(r"\w+", expected.lower()))
    act_words = set(re.findall(r"\w+", actual.lower()))
    if not exp_words:
        return 0.5
    overlap = len(exp_words & act_words) / len(exp_words)
    return round(1.0 - overlap, 2)


def _negative_tone(text: str) -> bool:
    """Returns True if the outcome text contains negative/disappointing language."""
    negatives = [
        "slower", "did not", "didn't", "failed", "worse", "unexpected", "challenging",
        "difficult", "struggle", "delay", "miss", "behind", "disappoint", "not as",
        "less than", "below", "overestimated", "underestimated", "unexpected",
    ]
    lower = text.lower()
    return any(n in lower for n in negatives)


def _detect_assumption_error(decision: Dict[str, Any], actual: str) -> str:
    """Identifies the likely assumption error from context."""
    assumptions = (decision.get("assumptions") or "").lower()
    reasoning = (decision.get("reasoning") or "").lower()
    actual_lower = actual.lower()

    if any(w in assumptions for w in ["quick", "fast", "easy", "immediately", "right away"]):
        return "the timeline assumption was optimistic — results took longer than planned"
    if any(w in assumptions for w in ["team", "people", "hire", "delegate", "va", "assistant"]):
        if any(w in actual_lower for w in ["onboard", "train", "ramp", "slow"]):
            return "the onboarding cost was underestimated — delegation has a hidden ramp-up phase"
    if any(w in reasoning for w in ["automat", "system", "tool", "software"]):
        return "adoption friction was not accounted for — tools and processes require integration time"
    if any(w in assumptions for w in ["revenue", "sales", "customer", "client"]):
        return "external response assumptions were too optimistic"

    return "the core assumption needed more validation before committing fully"


def _detect_cognitive_bias(decision: Dict[str, Any], actual: str) -> str:
    """Identifies the most likely cognitive bias that led to the gap."""
    confidence = decision.get("confidence_score", 50)
    expected = (decision.get("expected_outcome") or "").lower()
    actual_lower = actual.lower()

    if confidence >= 80 and _negative_tone(actual_lower):
        return "overconfidence bias — high confidence above 80% often masks unvalidated assumptions"
    if "automatically" in expected or "naturally" in expected:
        return "automation bias — assuming cause-and-effect would unfold without active management"
    if any(w in expected for w in ["immediately", "right away", "quickly", "within days"]):
        return "planning fallacy — underestimating the time and effort complex changes require"
    if "more focus" in expected or "more time" in expected or "freed up" in expected:
        return "opportunity neglect — assuming freed capacity automatically converts to strategic output"

    return "optimism bias — the expected outcome reflected best-case rather than realistic conditions"


# ── Public generators ─────────────────────────────────────────────────────────

def generate_reflection_insight_rule_based(
    decision: Dict[str, Any],
    actual_outcome: str,
    lessons: str,
) -> str:
    """Generate a sharp, original JARVIS reflection analysis from decision data."""
    title = decision.get("title", "this decision")
    expected = decision.get("expected_outcome", "")
    confidence = decision.get("confidence_score", 50)
    gap = _gap_score(expected, actual_outcome)
    negative = _negative_tone(actual_outcome)

    # Accuracy verdict
    if gap < 0.25:
        verdict = f"Your prediction for **{title}** was largely accurate"
        accuracy_note = "the fundamentals were sound, but execution complexity wasn't fully priced in"
    elif gap < 0.55:
        verdict = f"Your prediction for **{title}** partially held — some elements landed, others didn't"
        accuracy_note = "the direction was right but the magnitude and timeline were off"
    else:
        verdict = f"Your prediction for **{title}** diverged significantly from what actually happened"
        accuracy_note = "the mental model behind this decision needs revisiting"

    # Reasoning error
    assumption_error = _detect_assumption_error(decision, actual_outcome)
    bias = _detect_cognitive_bias(decision, actual_outcome)

    # Confidence calibration note
    if confidence >= 80 and negative:
        cal = f"Your {confidence}% confidence was not matched by the outcome — this is a calibration signal worth noting."
    elif confidence <= 40 and not negative:
        cal = f"You were uncertain ({confidence}% confidence) but the outcome was better than feared — trust your process more."
    else:
        cal = ""

    # Core actionable takeaway
    if "delegate" in title.lower() or "hire" in title.lower() or "assistant" in title.lower():
        takeaway = (
            "For future delegation decisions: document processes before hiring, "
            "define exactly how the freed time will be reinvested, and schedule "
            "strategic work in advance — delegation creates available time, not growth automatically."
        )
    elif "market" in title.lower() or "launch" in title.lower() or "campaign" in title.lower():
        takeaway = (
            "Before the next launch: validate the market signal with a small test, "
            "set measurable milestones weekly, and define what 'success' looks like at 30/60/90 days."
        )
    else:
        takeaway = (
            "For your next similar decision: write down exactly what needs to be true for your prediction "
            "to hold, then actively check each assumption before committing resources."
        )

    parts = [
        f"**JARVIS Analysis:** {verdict}. {accuracy_note.capitalize()}.",
        f"**Reasoning Error Detected:** {assumption_error.capitalize()}. This reflects {bias}.",
    ]
    if cal:
        parts.append(f"**Confidence Calibration:** {cal}")
    parts.append(f"**Strategic Takeaway:** {takeaway}")

    return "\n\n".join(parts)


def generate_replay_summary_rule_based(decisions: List[Dict], query: str) -> str:
    if not decisions:
        return f"No past decisions found matching '{query}'. Start capturing decisions to build your pattern library."

    categories = [d.get("category_tag", "Unknown") for d in decisions]
    cat_count: Dict[str, int] = {}
    for c in categories:
        cat_count[c] = cat_count.get(c, 0) + 1
    dominant = max(cat_count, key=cat_count.get)  # type: ignore

    reflected = [d for d in decisions if d.get("actual_outcome")]
    avg_sim = sum(d.get("similarity", 0) for d in decisions) / len(decisions)

    if reflected:
        outcomes = " | ".join(d.get("actual_outcome", "")[:60] for d in reflected[:2])
        pattern = f"Across {len(decisions)} similar decisions, your outcomes show: {outcomes}."
    else:
        pattern = f"You have {len(decisions)} similar past decisions but none have been reflected on yet — completing reflections will unlock pattern recognition."

    return (
        f"**Pattern for '{query}':** {len(decisions)} similar decisions found "
        f"({avg_sim:.0%} avg relevance), predominantly in **{dominant}**. "
        f"{pattern} "
        f"This cluster suggests a recurring decision pattern — review it before making the next similar move."
    )


def generate_alternative_strategy_rule_based(decision: Dict[str, Any]) -> str:
    title = decision.get("title", "this decision")
    reasoning = (decision.get("reasoning") or "").lower()
    expected = decision.get("expected_outcome", "")

    if any(w in reasoning for w in ["hire", "delegate", "assistant", "outsource"]):
        return (
            f"Instead of hiring immediately for **{title}**, a lower-risk alternative would have been "
            "to run a 30-day freelancer pilot on one defined task, measure the output quality and "
            "onboarding cost, then scale only after proving the ROI. This tests the delegation thesis "
            "with minimal commitment before a full structural change."
        )
    if any(w in reasoning for w in ["launch", "market", "campaign", "advertis"]):
        return (
            f"Rather than a full launch for **{title}**, a phased micro-launch to a small segment "
            "would have generated real market signal at low cost — validating assumptions before "
            "committing the full budget and timeline."
        )
    if any(w in reasoning for w in ["invest", "buy", "purchase", "tool", "software"]):
        return (
            f"An alternative to **{title}** would have been a time-boxed free trial or manual "
            "simulation of the outcome — proving the value hypothesis before investing, which reduces "
            "sunk-cost risk and sharpens the actual requirements."
        )

    return (
        f"An alternative approach to **{title}** would have been to break the decision into a "
        "smaller proof-of-concept phase first — testing the core assumption with 20% of the resources "
        "before full commitment. This de-risks the decision while still moving forward."
    )


def generate_daily_guidance_rule_based(
    query: str,
    similar_decisions: List[Dict],
    weekly_summary: Optional[Dict[str, Any]],
) -> Dict[str, str]:
    # High impact
    if similar_decisions:
        top = similar_decisions[0]
        high_impact = (
            f"Block 90 focused minutes on '{query}' — your past decision "
            f"'{top.get('title', 'similar work')}' shows this category drives your highest leverage outcomes."
        )
    else:
        high_impact = (
            f"Spend your first 90 minutes exclusively on '{query}' before checking messages, "
            "meetings, or email — deep focus early compounds throughout the day."
        )

    # Avoid busy work
    if weekly_summary:
        maintenance = weekly_summary.get("maintenance_pct", 0)
        if maintenance > 50:
            avoid = (
                f"Avoid operational tasks today — your week is already {maintenance:.0f}% maintenance. "
                "Protect this session for growth work only."
            )
        else:
            avoid = "Avoid unscheduled meetings and reactive Slack/email threads that fragment your focus."
    else:
        avoid = (
            "Avoid context-switching: keep your phone face-down, close non-essential tabs, "
            "and defer all non-urgent requests until after your focus block."
        )

    # Long-term alignment
    if similar_decisions and any(d.get("actual_outcome") for d in similar_decisions):
        reflected = next((d for d in similar_decisions if d.get("actual_outcome")), None)
        long_term = (
            f"Your work on '{query}' connects directly to a pattern you've been building — "
            f"past decisions like '{reflected.get('title', 'similar ones')}' show this is a "
            "recurring growth lever. Today's session reinforces that compounding trajectory."
        )
    else:
        long_term = (
            f"Every hour invested in '{query}' today is a vote for your 90-day goal. "
            "Small consistent actions in this area compound into the outcomes that matter most."
        )

    return {
        "high_impact": high_impact,
        "avoid_busy_work": avoid,
        "long_term_alignment": long_term,
    }


def generate_weekly_insight_rule_based(summary: Dict[str, Any]) -> str:
    maintenance = summary.get("maintenance_pct", 0)
    growth = summary.get("growth_pct", 0)
    strategic = summary.get("strategic_pct", 0)
    brand = summary.get("brand_pct", 0)
    admin = summary.get("admin_pct", 0)

    ratio = maintenance / max(growth + strategic, 1)

    if ratio > 4:
        tone = (
            f"⚠️ **Alert:** You spent {maintenance:.0f}% of your energy on maintenance vs "
            f"{growth + strategic:.0f}% on growth — a {ratio:.1f}x imbalance. "
            "At this rate, you're sustaining the business but not building it. "
            "Next week, protect at least one 3-hour growth block per day and treat it as non-negotiable."
        )
    elif ratio > 2:
        tone = (
            f"**Caution:** Maintenance ({maintenance:.0f}%) is eating twice the energy of growth "
            f"({growth + strategic:.0f}%). You're in operational mode. "
            "Identify one recurring maintenance task to systemize or delegate — "
            "that's your highest-leverage move this week."
        )
    elif growth + strategic > 40:
        tone = (
            f"✅ **Strong week:** {growth + strategic:.0f}% of your energy went toward growth and strategy. "
            f"Maintenance was contained at {maintenance:.0f}%. "
            "This is the ratio that builds momentum — protect this pattern and document what made it possible."
        )
    else:
        tone = (
            f"**Balanced week:** Maintenance {maintenance:.0f}% | Growth {growth:.0f}% | "
            f"Brand {brand:.0f}% | Admin {admin:.0f}%. "
            "The balance looks reasonable. To accelerate, shift 10% from admin into strategic work next week."
        )

    return tone
