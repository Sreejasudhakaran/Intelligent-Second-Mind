"use client";

import { useState, useEffect } from "react";
import AnimatedCard from "@/components/AnimatedCard";
import GradientButton from "@/components/GradientButton";
import InsightCard from "@/components/InsightCard";
import ProgressBar from "@/components/ProgressBar";
import { getWeeklyInsights, getPrinciples } from "@/lib/api";
import type { WeeklySummary } from "@/lib/types";
import { BarChart2, RefreshCw, BookOpen, Lock } from "lucide-react";

const METRICS = [
    { key: "maintenance_pct", label: "Maintenance (Busy)", colorClass: "bg-gray-400" },
    { key: "growth_pct", label: "Revenue Growth", colorClass: "bg-blue-500" },
    { key: "brand_pct", label: "Brand & Marketing", colorClass: "bg-purple-400" },
    { key: "admin_pct", label: "Admin & Planning", colorClass: "bg-orange-400" },
    { key: "strategic_pct", label: "Strategy", colorClass: "bg-green-500" },
] as const;

type Period = { key: string; label: string; sublabel: string };

const PERIODS: Period[] = [
    { key: "week", label: "Weekly", sublabel: "Last 7 days" },
    { key: "month", label: "Monthly", sublabel: "Last 30 days" },
    { key: "quarter", label: "Quarterly", sublabel: "Last 90 days" },
    { key: "year", label: "Yearly", sublabel: "Last 365 days" },
    { key: "all", label: "All Time", sublabel: "Since day one" },
];

export default function InsightsPage() {
    const [period, setPeriod] = useState("week");
    const [loading, setLoading] = useState(false);
    const [summary, setSummary] = useState<WeeklySummary | null>(null);
    const [aiInsight, setAiInsight] = useState("");
    const [recentInsights, setRecentInsights] = useState<
        { id: string; type: string; description: string; created_at: string }[]
    >([]);
    const [totalDecisions, setTotalDecisions] = useState(0);
    const [principles, setPrinciples] = useState<{ id: string; description: string; created_at: string }[]>([]);
    const [totalReflections, setTotalReflections] = useState(0);

    const load = async (p: string = period) => {
        setLoading(true);
        try {
            const [data, principlesData] = await Promise.all([
                getWeeklyInsights("default_user", p),
                getPrinciples("default_user"),
            ]);
            setSummary(data.summary);
            setAiInsight(data.ai_insight);
            setRecentInsights(data.recent_insights || []);
            setTotalDecisions((data.summary as any).total_decisions ?? 0);
            setPrinciples(principlesData.principles);
            setTotalReflections(principlesData.total_reflections);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { load(period); }, [period]);

    const maintenanceBusy = (summary?.maintenance_pct ?? 0) + (summary?.admin_pct ?? 0);
    const growthProactive = (summary?.growth_pct ?? 0) + (summary?.brand_pct ?? 0) + (summary?.strategic_pct ?? 0);
    const ratio = maintenanceBusy / Math.max(growthProactive, 1);
    const ratioText = ratio.toFixed(1);

    const currentPeriod = PERIODS.find((p) => p.key === period)!;

    const noData = !summary || totalDecisions === 0;

    return (
        <div className="max-w-2xl mx-auto">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">Pattern Intelligence</h1>
                    <p className="text-gray-400 text-sm mt-1">
                        Insight Layer · {currentPeriod.label} Busy vs Growth Analyzer
                    </p>
                </div>
                <GradientButton
                    variant="secondary"
                    onClick={() => load(period)}
                    loading={loading}
                    loadingText="Refreshing…"
                    size="sm"
                >
                    <RefreshCw size={14} />
                    Refresh
                </GradientButton>
            </div>

            {/* Period selector tabs */}
            <div className="flex gap-2 mb-6 bg-gray-100 rounded-xl p-1">
                {PERIODS.map((p) => (
                    <button
                        key={p.key}
                        onClick={() => setPeriod(p.key)}
                        className={`flex-1 py-2 px-1 rounded-lg text-xs font-semibold transition-all duration-200 ${period === p.key
                            ? "bg-white text-blue-600 shadow-sm"
                            : "text-gray-400 hover:text-gray-600"
                            }`}
                    >
                        {p.label}
                    </button>
                ))}
            </div>

            {/* No data state */}
            {noData && !loading && (
                <AnimatedCard className="p-8 text-center mb-6">
                    <BarChart2 size={32} className="text-gray-300 mx-auto mb-3" />
                    <p className="text-slate-700 font-semibold">No decisions in this period</p>
                    <p className="text-gray-400 text-sm mt-1">
                        Capture decisions in the {currentPeriod.label.toLowerCase()} view to see patterns here.
                    </p>
                </AnimatedCard>
            )}

            {/* Summary stats */}
            {!noData && summary && (
                <div className="grid grid-cols-2 gap-4 mb-6">
                    <AnimatedCard className="p-5 text-center" delay={0}>
                        <p className="text-3xl font-bold text-slate-800">{maintenanceBusy.toFixed(0)}%</p>
                        <p className="text-xs text-gray-400 mt-1">Busy Work</p>
                        <p className="text-[10px] text-gray-300 mt-0.5">Maintenance + Admin</p>
                    </AnimatedCard>
                    <AnimatedCard className="p-5 text-center" delay={0.05}>
                        <p className="text-3xl font-bold text-green-500">{growthProactive.toFixed(0)}%</p>
                        <p className="text-xs text-gray-400 mt-1">Growth</p>
                        <p className="text-[10px] text-gray-300 mt-0.5">Revenue + Brand + Strategy</p>
                    </AnimatedCard>
                </div>
            )}

            {/* Ratio banner */}
            {!noData && summary && (
                <AnimatedCard
                    delay={0.1}
                    className={`p-4 mb-6 border ${ratio > 2
                        ? "bg-orange-50 border-orange-100"
                        : ratio > 1
                            ? "bg-yellow-50 border-yellow-100"
                            : "bg-green-50 border-green-100"
                        }`}
                >
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <BarChart2
                                size={18}
                                className={ratio > 2 ? "text-orange-400" : ratio > 1 ? "text-yellow-500" : "text-green-500"}
                            />
                            <div>
                                <p className={`text-sm font-semibold ${ratio > 2 ? "text-orange-700" : ratio > 1 ? "text-yellow-700" : "text-green-700"}`}>
                                    {ratioText}x Busy vs Growth ratio
                                    {ratio < 0.5 ? " 🚀" : ratio > 3 ? " ⚠️" : ""}
                                </p>
                                <p className={`text-xs ${ratio > 2 ? "text-orange-400" : ratio > 1 ? "text-yellow-500" : "text-green-500"}`}>
                                    {ratio < 0.5
                                        ? "Excellent — growth is dominating your time."
                                        : ratio < 1
                                            ? "Good balance — growth focus is ahead of maintenance."
                                            : ratio < 2
                                                ? "Caution — maintenance is edging out growth work."
                                                : "Alert — you're spending significantly more time maintaining than growing."}
                                </p>
                            </div>
                        </div>
                        <span className="text-xs text-gray-400">
                            {totalDecisions} decision{totalDecisions !== 1 ? "s" : ""}
                        </span>
                    </div>
                </AnimatedCard>
            )}

            {/* Category breakdown bars */}
            {!noData && summary && (
                <AnimatedCard className="p-6 mb-6" delay={0.15}>
                    <h2 className="text-sm font-semibold text-slate-700 mb-4">
                        Category Breakdown · {currentPeriod.sublabel}
                    </h2>
                    {METRICS.map(({ key, label, colorClass }) => (
                        <ProgressBar
                            key={key}
                            label={label}
                            value={summary[key as keyof WeeklySummary] as number}
                            colorClass={colorClass}
                        />
                    ))}
                </AnimatedCard>
            )}

            {/* AI Insight */}
            {aiInsight && !aiInsight.includes("This week's activity was:") && (
                <InsightCard
                    insight={aiInsight}
                    label={`JARVIS ${currentPeriod.label} Insight`}
                    variant="blue"
                    className="mb-6"
                />
            )}

            {/* Recent insights */}
            {recentInsights.length > 0 && (
                <AnimatedCard className="p-5 mb-6" delay={0.2}>
                    <h2 className="text-sm font-semibold text-slate-700 mb-3">Recent Insights</h2>
                    <div className="space-y-3">
                        {recentInsights
                            .filter((ri) => !ri.description.includes("This week's activity was:"))
                            .map((ri) => (
                                <div key={ri.id} className="border-l-2 border-blue-200 pl-3">
                                    <p className="text-xs text-gray-400 mb-0.5">{ri.type}</p>
                                    <p className="text-sm text-slate-700">{ri.description}</p>
                                </div>
                            ))}
                    </div>
                </AnimatedCard>
            )}

            {/* ── Evolving Decision Principles ──────────────────────────────── */}
            <AnimatedCard className="p-6" delay={0.25}>
                <div className="flex items-center gap-2 mb-4">
                    <BookOpen size={16} className="text-blue-500" />
                    <h2 className="text-sm font-semibold text-slate-700">Your Evolving Decision Principles</h2>
                </div>

                {principles.length === 0 ? (
                    <div className="text-center py-4">
                        <Lock size={24} className="text-gray-300 mx-auto mb-2" />
                        <p className="text-sm text-slate-600 font-medium">
                            {totalReflections < 5
                                ? `${totalReflections}/5 reflections needed to unlock principles`
                                : "No principles extracted yet — submit a reflection to trigger extraction."}
                        </p>
                        {totalReflections < 5 && (
                            <div className="mt-3 bg-gray-100 rounded-full h-2 overflow-hidden">
                                <div
                                    className="bg-blue-400 h-2 rounded-full transition-all"
                                    style={{ width: `${(totalReflections / 5) * 100}%` }}
                                />
                            </div>
                        )}
                        <p className="text-xs text-gray-400 mt-2">
                            Reflect on past decisions to build your personal operating principles.
                        </p>
                    </div>
                ) : (
                    <div className="space-y-3">
                        {principles.map((p, idx) => (
                            <div
                                key={p.id}
                                className="border-l-4 border-blue-400 pl-4 py-2 bg-blue-50 rounded-r-xl"
                            >
                                <p className="text-xs font-semibold text-blue-500 mb-1">Principle #{idx + 1}</p>
                                <p className="text-sm text-slate-700 leading-relaxed">{p.description}</p>
                                <p className="text-[10px] text-gray-400 mt-1">
                                    Generated from {totalReflections} reflection{totalReflections !== 1 ? "s" : ""}
                                </p>
                            </div>
                        ))}
                    </div>
                )}
            </AnimatedCard>
        </div>
    );
}
