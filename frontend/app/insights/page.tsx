"use client";

import { useState, useEffect } from "react";
import AnimatedCard from "@/components/AnimatedCard";
import GradientButton from "@/components/GradientButton";
import InsightCard from "@/components/InsightCard";
import ProgressBar from "@/components/ProgressBar";
import { getWeeklyInsights } from "@/lib/api";
import type { WeeklySummary, RecentInsight } from "@/lib/types";
import { PROGRESS_BAR_COLORS } from "@/constants/colors";
import { BarChart2, RefreshCw } from "lucide-react";

const METRICS = [
    { key: "maintenance_pct", label: "Maintenance (Busy)", colorClass: "bg-gray-400" },
    { key: "growth_pct", label: "Revenue Growth", colorClass: "bg-blue-500" },
    { key: "brand_pct", label: "Brand & Marketing", colorClass: "bg-purple-400" },
    { key: "admin_pct", label: "Admin & Planning", colorClass: "bg-orange-400" },
    { key: "strategic_pct", label: "Strategy", colorClass: "bg-green-500" },
] as const;

export default function InsightsPage() {
    const [loading, setLoading] = useState(false);
    const [summary, setSummary] = useState<WeeklySummary | null>(null);
    const [aiInsight, setAiInsight] = useState("");
    const [recentInsights, setRecentInsights] = useState<RecentInsight[]>([]);

    const load = async () => {
        setLoading(true);
        try {
            const data = await getWeeklyInsights("default_user");
            setSummary(data.summary);
            setAiInsight(data.ai_insight);
            setRecentInsights(data.recent_insights || []);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { load(); }, []);

    const growthTotal = (summary?.growth_pct ?? 0) + (summary?.strategic_pct ?? 0);
    const maintenanceRatio = summary
        ? (summary.maintenance_pct / Math.max(growthTotal, 1)).toFixed(1)
        : null;

    return (
        <div className="max-w-2xl mx-auto">
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">Pattern Intelligence</h1>
                    <p className="text-gray-400 text-sm mt-1">Insight Layer · Weekly Busy vs Growth Analyzer</p>
                </div>
                <GradientButton variant="secondary" onClick={load} loading={loading} loadingText="Refreshing…" size="sm">
                    <RefreshCw size={14} />
                    Refresh
                </GradientButton>
            </div>

            {/* Summary stats */}
            {summary && (
                <div className="grid grid-cols-2 gap-4 mb-6">
                    <AnimatedCard className="p-5 text-center" delay={0}>
                        <p className="text-3xl font-bold text-slate-800">{summary.maintenance_pct.toFixed(0)}%</p>
                        <p className="text-xs text-gray-400 mt-1">Maintenance (Busy)</p>
                    </AnimatedCard>
                    <AnimatedCard className="p-5 text-center" delay={0.05}>
                        <p className="text-3xl font-bold text-green-500">{growthTotal.toFixed(0)}%</p>
                        <p className="text-xs text-gray-400 mt-1">Growth (Proactive)</p>
                    </AnimatedCard>
                </div>
            )}

            {/* Ratio banner */}
            {maintenanceRatio && (
                <AnimatedCard delay={0.1} className="p-4 mb-6 bg-orange-50 border border-orange-100">
                    <div className="flex items-center gap-2">
                        <BarChart2 size={18} className="text-orange-400" />
                        <div>
                            <p className="text-sm font-semibold text-orange-700">
                                {maintenanceRatio}x Maintenance vs Growth ratio
                            </p>
                            <p className="text-xs text-orange-400">{summary?.balance_label}</p>
                        </div>
                    </div>
                </AnimatedCard>
            )}

            {/* Progress bars */}
            <AnimatedCard className="p-6 mb-6" delay={0.15}>
                <h2 className="text-sm font-semibold text-slate-700 mb-4">Category Breakdown</h2>
                {summary ? (
                    METRICS.map(({ key, label, colorClass }) => (
                        <ProgressBar
                            key={key}
                            label={label}
                            value={summary[key as keyof WeeklySummary] as number}
                            colorClass={colorClass}
                        />
                    ))
                ) : (
                    <div className="space-y-4">
                        {METRICS.map(({ label }) => (
                            <div key={label} className="h-8 bg-gray-100 rounded animate-pulse" />
                        ))}
                    </div>
                )}
            </AnimatedCard>

            {/* AI Insight */}
            {aiInsight && (
                <InsightCard
                    insight={aiInsight}
                    label="JARVIS Weekly Insight"
                    variant="blue"
                    className="mb-6"
                />
            )}

            {/* Recent insights */}
            {recentInsights.length > 0 && (
                <AnimatedCard className="p-5" delay={0.2}>
                    <h2 className="text-sm font-semibold text-slate-700 mb-3">Recent Insights</h2>
                    <div className="space-y-3">
                        {recentInsights.map((ri) => (
                            <div key={ri.id} className="border-l-2 border-blue-200 pl-3">
                                <p className="text-xs text-gray-400 mb-0.5">{ri.type}</p>
                                <p className="text-sm text-slate-700">{ri.description}</p>
                            </div>
                        ))}
                    </div>
                </AnimatedCard>
            )}
        </div>
    );
}
