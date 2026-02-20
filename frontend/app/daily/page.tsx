"use client";

import { useState } from "react";
import AnimatedCard from "@/components/AnimatedCard";
import GradientButton from "@/components/GradientButton";
import InsightCard from "@/components/InsightCard";
import { getDailyGuidance } from "@/lib/api";
import type { DailyGuidance } from "@/lib/types";
import { getGreeting } from "@/lib/utils";
import { Compass, TrendingUp, ShieldOff, Target } from "lucide-react";

const guidanceItems = [
    { key: "high_impact", label: "High Impact Priority", icon: TrendingUp, color: "text-blue-500", bg: "bg-blue-50", border: "border-blue-100" },
    { key: "avoid_busy_work", label: "Avoid Busy Work", icon: ShieldOff, color: "text-orange-500", bg: "bg-orange-50", border: "border-orange-100" },
    { key: "long_term_alignment", label: "Long-Term Alignment", icon: Target, color: "text-green-500", bg: "bg-green-50", border: "border-green-100" },
] as const;

export default function DailyPage() {
    const [query, setQuery] = useState("");
    const [loading, setLoading] = useState(false);
    const [guidance, setGuidance] = useState<DailyGuidance | null>(null);
    const [context, setContext] = useState<{ similar_decisions_used?: number } | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;
        setLoading(true);
        setGuidance(null);
        try {
            const data = await getDailyGuidance(query, "default_user");
            setGuidance(data.guidance);
            setContext(data.context as { similar_decisions_used?: number });
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto">
            {/* Header */}
            <div className="mb-8">
                <p className="text-blue-500 font-semibold text-sm mb-1">{getGreeting()}</p>
                <h1 className="text-2xl font-bold text-slate-800">Daily Guidance</h1>
                <p className="text-gray-400 text-sm mt-1">Cognitive Layer · RAG-powered smart suggestions</p>
            </div>

            {/* Input */}
            <AnimatedCard className="p-6 mb-6">
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="text-sm font-semibold text-slate-700 block mb-2">
                            What's your focus today?
                        </label>
                        <textarea
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Describe your challenge, goal, or what's on your mind…"
                            rows={3}
                            className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm text-slate-700 resize-none focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition"
                            required
                        />
                    </div>
                    <GradientButton
                        type="submit"
                        loading={loading}
                        loadingText="Generating guidance with RAG…"
                        fullWidth
                    >
                        <Compass size={16} />
                        Generate Daily Guidance
                    </GradientButton>
                </form>
            </AnimatedCard>

            {/* Guidance cards */}
            {guidance && (
                <div className="space-y-4">
                    {guidanceItems.map(({ key, label, icon: Icon, color, bg, border }, i) => (
                        <AnimatedCard
                            key={key}
                            delay={i * 0.1}
                            className={`p-5 border ${border} ${bg}`}
                        >
                            <div className="flex items-center gap-2 mb-2">
                                <Icon size={18} className={color} />
                                <p className={`text-sm font-semibold ${color}`}>{label}</p>
                            </div>
                            <p className="text-sm text-slate-700 leading-relaxed">
                                {guidance[key as keyof DailyGuidance]}
                            </p>
                        </AnimatedCard>
                    ))}

                    {/* Context meta */}
                    {context && (
                        <div className="px-1">
                            <p className="text-xs text-gray-400">
                                Powered by {context.similar_decisions_used ?? 0} similar past decisions from your memory
                            </p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
