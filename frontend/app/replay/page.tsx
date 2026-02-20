"use client";

import { useState } from "react";
import AnimatedCard from "@/components/AnimatedCard";
import GradientButton from "@/components/GradientButton";
import DecisionCard from "@/components/DecisionCard";
import InsightCard from "@/components/InsightCard";
import { replaySimilar, getAlternativeStrategy } from "@/lib/api";
import type { Decision } from "@/lib/types";
import { Search, Lightbulb } from "lucide-react";

export default function ReplayPage() {
    const [query, setQuery] = useState("");
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState<Decision[]>([]);
    const [summary, setSummary] = useState("");
    const [altStrategy, setAltStrategy] = useState<{ id: string; text: string } | null>(null);
    const [altLoading, setAltLoading] = useState<string | null>(null);

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;
        setLoading(true);
        setSummary("");
        setResults([]);
        try {
            const data = await replaySimilar(query, "default_user");
            setResults(data.decisions);
            setSummary(data.pattern_summary);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleAlternative = async (decisionId: string) => {
        setAltLoading(decisionId);
        try {
            const data = await getAlternativeStrategy(decisionId);
            setAltStrategy({ id: decisionId, text: data.alternative_strategy });
        } catch (err) {
            console.error(err);
        } finally {
            setAltLoading(null);
        }
    };

    return (
        <div className="max-w-2xl mx-auto">
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-slate-800">Decision Replay</h1>
                <p className="text-gray-400 text-sm mt-1">Recall Layer · Search similar past decisions via vector similarity</p>
            </div>

            {/* Search */}
            <AnimatedCard className="p-6 mb-6">
                <form onSubmit={handleSearch} className="space-y-4">
                    <div>
                        <label className="text-sm font-semibold text-slate-700 block mb-2">
                            Search Similar Decisions
                        </label>
                        <div className="flex gap-3">
                            <div className="relative flex-1">
                                <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                                <input
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    placeholder="Describe a situation or topic…"
                                    className="w-full border border-gray-200 rounded-xl pl-9 pr-4 py-3 text-sm text-slate-700 focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition"
                                    required
                                />
                            </div>
                            <GradientButton type="submit" loading={loading} loadingText="Searching…">
                                Search
                            </GradientButton>
                        </div>
                    </div>
                </form>
            </AnimatedCard>

            {/* Pattern summary */}
            {summary && (
                <InsightCard
                    insight={summary}
                    label="Pattern Observation"
                    variant="blue"
                    className="mb-6"
                />
            )}

            {/* Alt strategy */}
            {altStrategy && (
                <InsightCard
                    insight={altStrategy.text}
                    label="Alternative Strategy"
                    variant="orange"
                    className="mb-6"
                />
            )}

            {/* Results */}
            {results.length > 0 && (
                <div className="space-y-3">
                    <p className="text-sm font-semibold text-gray-500 mb-4">
                        Top {results.length} similar decisions
                    </p>
                    {results.map((d) => (
                        <DecisionCard
                            key={d.id}
                            decision={d}
                            showSimilarity
                            actions={
                                <button
                                    onClick={() => handleAlternative(d.id)}
                                    disabled={altLoading === d.id}
                                    className="flex items-center gap-1 text-xs text-orange-500 hover:text-orange-600 font-medium transition disabled:opacity-50"
                                >
                                    <Lightbulb size={12} />
                                    {altLoading === d.id ? "Generating…" : "Alternative"}
                                </button>
                            }
                        />
                    ))}
                </div>
            )}

            {!loading && query && results.length === 0 && (
                <AnimatedCard className="p-8 text-center">
                    <p className="text-gray-400 text-sm">No similar decisions found. Try a different query.</p>
                </AnimatedCard>
            )}
        </div>
    );
}
