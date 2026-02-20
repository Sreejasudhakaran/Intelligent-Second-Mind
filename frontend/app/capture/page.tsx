"use client";

import { useState } from "react";
import AnimatedCard from "@/components/AnimatedCard";
import GradientButton from "@/components/GradientButton";
import VoiceRecorder from "@/components/VoiceRecorder";
import InsightCard from "@/components/InsightCard";
import { createDecision } from "@/lib/api";
import { CATEGORIES, CATEGORY_ICONS } from "@/constants/categories";
import { Sparkles, RotateCcw, AlertTriangle } from "lucide-react";

type DecisionType = "reversible" | "irreversible";

export default function CapturePage() {
    const [form, setForm] = useState({
        title: "",
        reasoning: "",
        assumptions: "",
        expected_outcome: "",
        confidence_score: 70,
    });
    const [decisionType, setDecisionType] = useState<DecisionType>("reversible");
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);

    const appendVoice = (field: keyof typeof form) => (text: string) => {
        setForm((f) => ({ ...f, [field]: f[field] ? f[field] + " " + text : text }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!form.title.trim()) return;
        setLoading(true);
        try {
            await createDecision({ ...form, user_id: "default_user", decision_type: decisionType });
            setSuccess(true);
            setForm({ title: "", reasoning: "", assumptions: "", expected_outcome: "", confidence_score: 70 });
            setDecisionType("reversible");
            setTimeout(() => setSuccess(false), 4000);
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
                <h1 className="text-2xl font-bold text-slate-800">Decision Capture</h1>
                <p className="text-gray-400 text-sm mt-1">Memory Layer · Record your decision with full context</p>
            </div>

            {success && (
                <InsightCard
                    insight="Decision captured and embedded successfully."
                    label="Saved"
                    variant="green"
                    className="mb-6"
                />
            )}

            <AnimatedCard className="p-6 mb-6">
                <form onSubmit={handleSubmit} className="space-y-5">
                    {/* Title + Voice */}
                    <div>
                        <div className="flex items-center justify-between mb-2">
                            <label className="text-sm font-semibold text-slate-700">
                                Decision Title <span className="text-red-400">*</span>
                            </label>
                            <VoiceRecorder onTranscript={appendVoice("title")} />
                        </div>
                        <input
                            value={form.title}
                            onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
                            placeholder="What decision are you making?"
                            className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm text-slate-700 focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition"
                            required
                        />
                    </div>

                    {/* ── Decision Nature Toggle ───────────────────────────────── */}
                    <div>
                        <label className="text-sm font-semibold text-slate-700 block mb-2">Decision Nature</label>
                        <div className="flex rounded-full bg-gray-100 p-1 gap-1">
                            <button
                                type="button"
                                onClick={() => setDecisionType("reversible")}
                                title="Can be undone easily — favour speed and experimentation"
                                className={`flex-1 flex items-center justify-center gap-2 py-2 rounded-full text-sm font-semibold transition-all duration-200 ${decisionType === "reversible"
                                    ? "bg-white text-blue-600 shadow-sm"
                                    : "text-gray-400 hover:text-gray-600"
                                    }`}
                            >
                                <RotateCcw size={14} />
                                Reversible
                            </button>
                            <button
                                type="button"
                                onClick={() => setDecisionType("irreversible")}
                                title="Hard to undo — high long-term impact, requires careful thinking"
                                className={`flex-1 flex items-center justify-center gap-2 py-2 rounded-full text-sm font-semibold transition-all duration-200 ${decisionType === "irreversible"
                                    ? "bg-white text-orange-500 shadow-sm"
                                    : "text-gray-400 hover:text-gray-600"
                                    }`}
                            >
                                <AlertTriangle size={14} />
                                Irreversible
                            </button>
                        </div>
                        <p className="text-xs text-gray-400 mt-1.5 text-center">
                            {decisionType === "reversible"
                                ? "↻ Can be undone — JARVIS encourages fast iteration"
                                : "⚠ Hard to undo — JARVIS will evaluate risks and long-term impact"}
                        </p>
                    </div>

                    {/* Reasoning */}
                    <div>
                        <div className="flex items-center gap-2 mb-2">
                            <label className="text-sm font-semibold text-slate-700">Reasoning</label>
                            <VoiceRecorder compact onTranscript={appendVoice("reasoning")} />
                        </div>
                        <textarea
                            value={form.reasoning}
                            onChange={(e) => setForm((f) => ({ ...f, reasoning: e.target.value }))}
                            placeholder="Why are you making this decision?"
                            rows={3}
                            className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm text-slate-700 resize-none focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition"
                        />
                    </div>

                    {/* Assumptions */}
                    <div>
                        <div className="flex items-center gap-2 mb-2">
                            <label className="text-sm font-semibold text-slate-700">Assumptions</label>
                            <VoiceRecorder compact onTranscript={appendVoice("assumptions")} />
                        </div>
                        <textarea
                            value={form.assumptions}
                            onChange={(e) => setForm((f) => ({ ...f, assumptions: e.target.value }))}
                            placeholder="What are you assuming to be true?"
                            rows={2}
                            className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm text-slate-700 resize-none focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition"
                        />
                    </div>

                    {/* Expected Outcome */}
                    <div>
                        <div className="flex items-center gap-2 mb-2">
                            <label className="text-sm font-semibold text-slate-700">Expected Outcome</label>
                            <VoiceRecorder compact onTranscript={appendVoice("expected_outcome")} />
                        </div>
                        <textarea
                            value={form.expected_outcome}
                            onChange={(e) => setForm((f) => ({ ...f, expected_outcome: e.target.value }))}
                            placeholder="What result do you expect?"
                            rows={2}
                            className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm text-slate-700 resize-none focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition"
                        />
                    </div>

                    {/* Confidence */}
                    <div>
                        <label className="text-sm font-semibold text-slate-700 block mb-2">
                            Confidence <span className="text-blue-500 font-bold">{form.confidence_score}%</span>
                        </label>
                        <input
                            type="range"
                            min="0"
                            max="100"
                            step="5"
                            value={form.confidence_score}
                            onChange={(e) => setForm((f) => ({ ...f, confidence_score: Number(e.target.value) }))}
                            className="w-full accent-blue-500"
                        />
                        <div className="flex justify-between text-xs text-gray-400 mt-1">
                            <span>Not sure</span><span>Very confident</span>
                        </div>
                    </div>

                    <GradientButton
                        type="submit"
                        loading={loading}
                        loadingText="Capturing decision…"
                        fullWidth
                    >
                        <Sparkles size={16} />
                        Capture Decision
                    </GradientButton>
                </form>
            </AnimatedCard>

            {/* Category info */}
            <AnimatedCard delay={0.15} className="p-5">
                <p className="text-xs font-semibold text-gray-400 mb-3">Auto-tagged into categories</p>
                <div className="grid grid-cols-3 gap-2">
                    {CATEGORIES.slice(0, 5).map((c) => (
                        <div key={c} className="bg-gray-50 rounded-lg px-3 py-2 text-center">
                            <span className="text-lg">{CATEGORY_ICONS[c]}</span>
                            <p className="text-[10px] text-gray-500 mt-1 leading-tight">{c}</p>
                        </div>
                    ))}
                </div>
            </AnimatedCard>
        </div>
    );
}
