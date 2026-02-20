"use client";

import { motion } from "framer-motion";
import { clampPercent } from "@/lib/utils";

interface ProgressBarProps {
    label: string;
    value: number;
    colorClass?: string;
    showLabel?: boolean;
    animate?: boolean;
}

export default function ProgressBar({
    label,
    value,
    colorClass = "bg-blue-500",
    showLabel = true,
    animate = true,
}: ProgressBarProps) {
    const clamped = clampPercent(value);

    return (
        <div className="mb-5">
            {showLabel && (
                <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-slate-700">{label}</span>
                    <span className="text-sm font-semibold text-slate-600">{clamped.toFixed(0)}%</span>
                </div>
            )}
            <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
                {animate ? (
                    <motion.div
                        className={`h-3 rounded-full ${colorClass}`}
                        initial={{ width: 0 }}
                        animate={{ width: `${clamped}%` }}
                        transition={{ duration: 0.8, ease: "easeOut" }}
                    />
                ) : (
                    <div className={`h-3 rounded-full ${colorClass}`} style={{ width: `${clamped}%` }} />
                )}
            </div>
        </div>
    );
}
