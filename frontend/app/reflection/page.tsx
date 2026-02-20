"use client";

import { useState, useEffect } from "react";
import AnimatedCard from "@/components/AnimatedCard";
import GradientButton from "@/components/GradientButton";
import InsightCard from "@/components/InsightCard";
import { listDecisions, createReflection, getReflection } from "@/lib/api";
import type { Decision, Reflection } from "@/lib/types";
import { formatDate } from "@/lib/utils";
import { ChevronDown } from "lucide-react";

export default function ReflectionPage() {
    const [decisions, setDecisions] = useState<Decision[]>([]);
    const [selected, setSelected] = useState<string>("");
    const [actualOutcome, setActualOutcome] = useState("");
    const [lessons, setLessons] = useState("");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<Reflection | null>(null);

    useEffect(() => {
        listDecisions("default_user").then(setDecisions).catch(console.error);
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selected || !actualOutcome.trim()) return;
        setLoading(true);
        try {
            const r = await createReflection({ decision_id: selected, actual_outcome: actualOutcome, lessons });
            setResult(r);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const selectedDecision = decisions.find((d) => d.id === selected);

    return (
        <div className="max-w-2xl mx-auto">
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-slate-800">Reflection Engine</h1>
                <p className="text-gray-400 text-sm mt-1">Learning Layer · Compare expected vs actual outcomes</p>
            </div>

            <AnimatedCard className="p-6 mb-6">
                <form onSubmit={handleSubmit} className="space-y-5">
                    {/* Decision selector */}
                    <div>
                        <label className="text-sm font-semibold text-slate-700 block mb-2">Select Decision</label>
                        <div className="relative">
                            <select
                                value={selected}
                                onChange={(e) => setSelected(e.target.value)}
                                className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm text-slate-700 bg-white focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 appearance-none"
                                required
                            >
                                <option value="">Choose a past decision…</option>
                                {decisions.map((d) => (
                                    <option key={d.id} value={d.id}>
                                        {d.title} · {d.category_tag}
                                    </option>
                                ))}
                            </select>
                            <ChevronDown size={16} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" />
                        </div>
                    </div>

                    {/* Expected outcome preview */}
                    {selectedDecision?.expected_outcome && (
                        <div className="bg-gray-50 rounded-xl p-4">
                            <p className="text-xs font-medium text-gray-400 mb-1">Expected outcome</p>
                            <p className="text-sm text-slate-700">{selectedDecision.expected_outcome}</p>
                        </div>
                    )}

                    {/* Actual outcome */}
                    <div>
                        <label className="text-sm font-semibold text-slate-700 block mb-2">Actual Outcome</label>
                        <textarea
                            value={actualOutcome}
                            onChange={(e) => setActualOutcome(e.target.value)}
                            placeholder="What actually happened?"
                            rows={3}
                            className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm text-slate-700 resize-none focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition"
                            required
                        />
                    </div>

                    {/* Lessons */}
                    <div>
                        <label className="text-sm font-semibold text-slate-700 block mb-2">Lessons Learned</label>
                        <textarea
                            value={lessons}
                            onChange={(e) => setLessons(e.target.value)}
                            placeholder="What did you learn from this?"
                            rows={2}
                            className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm text-slate-700 resize-none focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition"
                        />
                    </div>

                    <GradientButton
                        type="submit"
                        loading={loading}
                        loadingText="Analyzing with AI…"
                        fullWidth
                    >
                        Generate AI Insight
                    </GradientButton>
                </form>
            </AnimatedCard>

            {result && (
                <div className="space-y-4">
                    {result.ai_insight && (
                        <InsightCard insight={result.ai_insight} label="JARVIS Analysis" variant="blue" />
                    )}
                    <AnimatedCard className="p-5">
                        <div className="grid grid-cols-2 gap-4 text-sm">
                            <div>
                                <p className="text-xs text-gray-400 mb-1">Accuracy Score</p>
                                <p className="text-2xl font-bold text-blue-500">{result.accuracy_score ?? "—"}%</p>
                            </div>
                            <div>
                                <p className="text-xs text-gray-400 mb-1">Reflected on</p>
                                <p className="font-medium text-slate-700">{formatDate(result.created_at)}</p>
                            </div>
                        </div>
                    </AnimatedCard>
                </div>
            )}
        </div>
    );
}
