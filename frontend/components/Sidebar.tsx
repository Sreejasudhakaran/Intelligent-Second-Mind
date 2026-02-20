"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import {
    ClipboardList,
    RotateCcw,
    Play,
    BarChart2,
    Sunrise,
    Zap,
} from "lucide-react";

const navItems = [
    { href: "/capture", label: "Decision Capture", icon: ClipboardList, sub: "Memory Layer" },
    { href: "/reflection", label: "Reflection Engine", icon: RotateCcw, sub: "Learning Layer" },
    { href: "/replay", label: "Decision Replay", icon: Play, sub: "Recall Layer" },
    { href: "/insights", label: "Pattern Intelligence", icon: BarChart2, sub: "Insight Layer" },
    { href: "/daily", label: "Daily Guidance", icon: Sunrise, sub: "Cognitive Layer" },
];

export default function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="fixed left-0 top-0 h-screen w-64 bg-white border-r border-gray-100 shadow-card flex flex-col z-50">
            {/* Logo */}
            <div className="px-6 py-7 border-b border-gray-100">
                <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center shadow-blue-glow">
                        <Zap size={18} className="text-white" />
                    </div>
                    <div>
                        <h1 className="text-lg font-bold text-slate-900 leading-none">JARVIS</h1>
                        <p className="text-xs text-gray-400 mt-0.5">Decision Intelligence</p>
                    </div>
                </div>
            </div>

            {/* Navigation */}
            <nav className="flex-1 px-3 py-5 space-y-1 overflow-y-auto">
                {navItems.map((item) => {
                    const isActive = pathname === item.href;
                    const Icon = item.icon;
                    return (
                        <Link key={item.href} href={item.href}>
                            <motion.div
                                whileHover={{ x: 3 }}
                                whileTap={{ scale: 0.98 }}
                                className={`flex items-center gap-3 px-3 py-3 rounded-xl cursor-pointer transition-colors duration-150 ${isActive
                                        ? "bg-blue-50 text-blue-600"
                                        : "text-gray-600 hover:bg-gray-50 hover:text-slate-800"
                                    }`}
                            >
                                <div
                                    className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${isActive ? "bg-blue-100" : "bg-gray-100"
                                        }`}
                                >
                                    <Icon size={16} className={isActive ? "text-blue-600" : "text-gray-500"} />
                                </div>
                                <div className="min-w-0">
                                    <p className={`text-sm font-medium truncate ${isActive ? "text-blue-700" : ""}`}>
                                        {item.label}
                                    </p>
                                    <p className="text-xs text-gray-400 truncate">{item.sub}</p>
                                </div>
                                {isActive && (
                                    <div className="ml-auto w-1.5 h-1.5 rounded-full bg-blue-500 flex-shrink-0" />
                                )}
                            </motion.div>
                        </Link>
                    );
                })}
            </nav>

            {/* Footer */}
            <div className="px-5 py-4 border-t border-gray-100">
                <p className="text-xs text-gray-400 text-center">
                    4-Layer Cognitive Architecture
                </p>
            </div>
        </aside>
    );
}
