export interface Decision {
    id: string;
    title: string;
    reasoning?: string;
    assumptions?: string;
    expected_outcome?: string;
    confidence_score?: number;
    category_tag?: string;
    decision_type?: string;   // "reversible" | "irreversible" — auto-classified by backend
    created_at?: string;
    user_id: string;
    similarity?: number;
    actual_outcome?: string;
    lessons?: string;
}

export interface Reflection {
    id: string;
    decision_id: string;
    actual_outcome: string;
    lessons?: string;
    accuracy_score?: number;
    ai_insight?: string;
    created_at: string;
}

export interface WeeklySummary {
    maintenance_pct: number;
    growth_pct: number;
    brand_pct: number;
    admin_pct: number;
    strategic_pct: number;
    week_start?: string;
    balance_label?: string;
}

export interface DailyGuidance {
    high_impact: string;
    avoid_busy_work: string;
    long_term_alignment: string;
}

export interface InsightEntry {
    id: string;
    type: string;
    description: string;
    created_at: string;
}

export interface RecentInsight {
    id: string;
    type: string;
    description: string;
    created_at: string;
}
