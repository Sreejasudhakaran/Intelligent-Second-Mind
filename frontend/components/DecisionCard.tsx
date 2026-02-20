"use client";

import { motion } from "framer-motion";
import { Tag, Calendar, TrendingUp } from "lucide-react";
import type { Decision } from "@/lib/types";
import { formatDate } from "@/lib/utils";
import { CATEGORY_ICONS } from "@/constants/categories";
import { PROGRESS_BAR_COLORS } from "@/constants/colors";

interface DecisionCardProps {
    decision: Decision;
    showSimilarity?: boolean;
    actions?: React.ReactNode;
    className?: string;
}

export default function DecisionCard({
    decision,
    showSimilarity = false,
    actions,
    className = "",
}: DecisionCardProps) {
    const icon = CATEGORY_ICONS[decision.category_tag as keyof typeof CATEGORY_ICONS] || "🎯";

    return (
        <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className={`bg-gray-50 rounded-xl p-5 border border-gray-100 hover:border-blue-200 transition-colors duration-200 ${className}`}
        >
            {/* Header */}
            <div className="flex items-start justify-between gap-3 mb-3">
                <div className="flex items-start gap-2 flex-1 min-w-0">
                    <span className="text-lg mt-0.5 flex-shrink-0">{icon}</span>
                    <div className="min-w-0">
                        <h3 className="font-semibold text-slate-800 text-sm leading-snug truncate">
                            {decision.title}
                        </h3>
                        {decision.category_tag && (
                            <span className="inline-flex items-center gap-1 text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full mt-1">
                                <Tag size={9} />
                                {decision.category_tag}
                            </span>
                        )}
                    </div>
                </div>
                {showSimilarity && decision.similarity !== undefined && (
                    <div className="flex items-center gap-1 flex-shrink-0">
                        <TrendingUp size={12} className="text-blue-400" />
                        <span className="text-xs font-semibold text-blue-500">
                            {(decision.similarity * 100).toFixed(0)}%
                        </span>
                    </div>
                )}
            </div>

            {/* Outcomes */}
            <div className="grid grid-cols-2 gap-2 mb-3 text-xs text-gray-600">
                <div className="bg-white rounded-lg p-2.5">
                    <p className="font-medium text-gray-400 mb-0.5">Expected</p>
                    <p className="text-slate-700">{decision.expected_outcome || "N/A"}</p>
                </div>
                <div className="bg-white rounded-lg p-2.5">
                    <p className="font-medium text-gray-400 mb-0.5">Actual</p>
                    <p className="text-slate-700">{decision.actual_outcome || "Not yet reflected"}</p>
                </div>
            </div>

            {/* Footer */}
            <div className="flex items-center justify-between">
                {decision.created_at && (
                    <div className="flex items-center gap-1 text-xs text-gray-400">
                        <Calendar size={11} />
                        {formatDate(decision.created_at)}
                    </div>
                )}
                {actions && <div>{actions}</div>}
            </div>
        </motion.div>
    );
}
