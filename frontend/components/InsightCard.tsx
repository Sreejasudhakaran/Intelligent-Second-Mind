"use client";

import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

interface InsightCardProps {
    insight: string;
    label?: string;
    variant?: "blue" | "green" | "orange";
    className?: string;
}

const variantStyles = {
    blue: "border-blue-200 bg-blue-50 text-blue-700",
    green: "border-green-200 bg-green-50 text-green-700",
    orange: "border-orange-200 bg-orange-50 text-orange-700",
};

const sparkleColors = {
    blue: "text-blue-500",
    green: "text-green-500",
    orange: "text-orange-500",
};

export default function InsightCard({
    insight,
    label = "AI Insight",
    variant = "blue",
    className = "",
}: InsightCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className={`border rounded-2xl p-5 ${variantStyles[variant]} ${className}`}
        >
            <div className="flex items-center gap-2 mb-2">
                <Sparkles size={16} className={sparkleColors[variant]} />
                <p className="text-sm font-semibold">{label}</p>
            </div>
            <p className="text-sm leading-relaxed opacity-90">{insight}</p>
        </motion.div>
    );
}
