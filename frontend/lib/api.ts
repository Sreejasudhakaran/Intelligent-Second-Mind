import axios from "axios";
import type { Decision, Reflection, WeeklySummary, DailyGuidance } from "./types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const client = axios.create({
    baseURL: BASE_URL,
    headers: { "Content-Type": "application/json" },
});

// ── Decisions ─────────────────────────────────────────────
export interface DecisionPayload {
    title: string;
    reasoning?: string;
    assumptions?: string;
    expected_outcome?: string;
    confidence_score?: number;
    user_id?: string;
    decision_type?: string;  // reversible | irreversible
}

export const createDecision = (data: DecisionPayload): Promise<Decision> =>
    client.post("/decisions/", data).then((r) => r.data);

export const listDecisions = (user_id = "default_user"): Promise<Decision[]> =>
    client.get(`/decisions/?user_id=${user_id}`).then((r) => r.data);

export const getDecision = (id: string): Promise<Decision> =>
    client.get(`/decisions/${id}`).then((r) => r.data);

// ── Reflections ───────────────────────────────────────────
export interface ReflectionPayload {
    decision_id: string;
    actual_outcome: string;
    lessons?: string;
    accuracy_score?: number;
    user_id?: string;
}

export const createReflection = (data: ReflectionPayload): Promise<Reflection> =>
    client.post("/reflections/", data).then((r) => r.data);

export const getReflection = (decision_id: string): Promise<Reflection> =>
    client.get(`/reflections/${decision_id}`).then((r) => r.data);

// ── Replay ────────────────────────────────────────────────
export const replaySimilar = (query: string, user_id = "default_user", top_k = 5) =>
    client
        .post("/replay/similar", { query, user_id, top_k })
        .then((r) => r.data as { query: string; decisions: Decision[]; pattern_summary: string });

export const getAlternativeStrategy = (decision_id: string) =>
    client
        .post(`/replay/alternative?decision_id=${decision_id}`)
        .then((r) => r.data as { decision_id: string; alternative_strategy: string });

// ── Insights ──────────────────────────────────────────────
export const getWeeklyInsights = (user_id = "default_user", period = "week") =>
    client.get(`/insights/weekly?user_id=${user_id}&period=${period}`).then(
        (r) =>
            r.data as {
                summary: WeeklySummary;
                ai_insight: string;
                recent_insights: { id: string; type: string; description: string; created_at: string }[];
            }
    );

export const getPrinciples = (user_id = "default_user") =>
    client.get(`/insights/principles?user_id=${user_id}`).then(
        (r) => r.data as {
            principles: { id: string; description: string; created_at: string }[];
            total_reflections: number;
            extraction_threshold: number;
        }
    );

// ── Daily Guidance ────────────────────────────────────────
export const getDailyGuidance = (
    query: string,
    user_id = "default_user"
) =>
    client
        .post("/daily/guidance", { query, user_id })
        .then((r) => r.data as { query: string; guidance: DailyGuidance; context: object });
