"use client";

import { useState } from "react";
import AnimatedCard from "@/components/AnimatedCard";
import GradientButton from "@/components/GradientButton";
import VoiceRecorder from "@/components/VoiceRecorder";
import { createDecision } from "@/lib/api";
import type { Decision } from "@/lib/types";
import { CATEGORIES, CATEGORY_ICONS } from "@/constants/categories";
import { Sparkles, RotateCcw, AlertTriangle, CheckCircle2 } from "lucide-react";

export default function CapturePage() {
    const [form, setForm] = useState({
        title: "",
        reasoning: "",
        assumptions: "",
        expected_outcome: "",
        confidence_score: 70,
    });
    const [loading, setLoading] = useState(false);
    const [saved, setSaved] = useState<Decision | null>(null);

    const appendVoice = (field: keyof typeof form) => (text: string) => {
        setForm((f) => ({ ...f, [field]: f[field] ? f[field] + " " + text : text }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!form.title.trim()) return;
        setLoading(true);
        try {
            const result = await createDecision({ ...form, user_id: "default_user" });
            setSaved(result);
            setForm({ title: "", reasoning: "", assumptions: "", expected_outcome: "", confidence_score: 70 });
            setTimeout(() => setSaved(null), 8000);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const isIrreversible = saved?.decision_type === "irreversible";

    return (
        <div className="max-w-2xl mx-auto">
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-slate-800">Decision Capture</h1>
                <p className="text-gray-400 text-sm mt-1">Memory Layer · Record your decision with full context</p>
            </div>

            {/* ── Auto-classified badge shown after save ── */}
            {saved && (
                <div className="mb-6 flex items-center gap-3">
                    {/* Category badge */}
                    <span className="inline-flex items-center gap-1.5 bg-blue-50 border border-blue-200 text-blue-600 text-xs font-semibold px-3 py-1.5 rounded-full shadow-sm">
                        <CheckCircle2 size={12} />
                        Saved · {saved.category_tag ?? "Uncategorised"}
                    </span>

                    {/* Reversibility badge */}
                    {isIrreversible ? (
                        <span className="inline-flex items-center gap-1.5 bg-orange-50 border border-orange-200 text-orange-500 text-xs font-semibold px-3 py-1.5 rounded-full shadow-sm">
                            <AlertTriangle size={12} />
                            Irreversible Decision — High long-term commitment
                        </span>
                    ) : (
                        <span className="inline-flex items-center gap-1.5 bg-green-50 border border-green-200 text-green-600 text-xs font-semibold px-3 py-1.5 rounded-full shadow-sm">
                            <RotateCcw size={12} />
                            Reversible Decision — Safe to iterate
                        </span>
                    )}
                </div>
            )}

            <AnimatedCard className="p-6 mb-6">
                <form onSubmit={handleSubmit} className="space-y-5">
                    {/* Title */}
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
                            type="range" min="0" max="100" step="5"
                            value={form.confidence_score}
                            onChange={(e) => setForm((f) => ({ ...f, confidence_score: Number(e.target.value) }))}
                            className="w-full accent-blue-500"
                        />
                        <div className="flex justify-between text-xs text-gray-400 mt-1">
                            <span>Not sure</span><span>Very confident</span>
                        </div>
                    </div>

                    <GradientButton type="submit" loading={loading} loadingText="Capturing decision…" fullWidth>
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
                <p className="text-[10px] text-gray-400 mt-3 text-center">
                    Reversibility is auto-detected from your decision context
                </p>
            </AnimatedCard>
        </div>
    );
}
