"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Brain, Mic, RotateCcw, BarChart2, Compass } from "lucide-react";
import { cn } from "@/lib/utils";

const nav = [
    { href: "/capture", icon: Mic, label: "Decision Capture", sub: "Memory Layer" },
    { href: "/reflection", icon: Brain, label: "Reflection Engine", sub: "Learning Layer" },
    { href: "/replay", icon: RotateCcw, label: "Decision Replay", sub: "Recall Layer" },
    { href: "/insights", icon: BarChart2, label: "Pattern Insights", sub: "Pattern Layer" },
    { href: "/daily", icon: Compass, label: "Daily Guidance", sub: "Cognitive Layer" },
];

export default function Sidebar() {
    const path = usePathname();

    return (
        <aside className="w-64 fixed top-0 left-0 h-screen bg-white/80 backdrop-blur-md border-r border-gray-100 flex flex-col py-6 px-4 shadow-sm z-50">
            {/* Brand */}
            <div className="flex items-center gap-3 mb-8 px-2">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center shadow-md">
                    <span className="text-white font-bold text-sm">J</span>
                </div>
                <div>
                    <p className="font-bold text-slate-800 text-base leading-tight">JARVIS</p>
                    <p className="text-xs text-gray-400">Decision Intelligence</p>
                </div>
            </div>

            {/* Navigation */}
            <nav className="flex-1 space-y-1">
                {nav.map(({ href, icon: Icon, label, sub }) => {
                    const active = path.startsWith(href);
                    return (
                        <Link
                            key={href}
                            href={href}
                            className={cn(
                                "flex items-center gap-3 px-3 py-3 rounded-xl text-sm transition-all duration-200 group",
                                active
                                    ? "bg-blue-50 text-blue-600"
                                    : "text-slate-500 hover:bg-gray-50 hover:text-slate-700"
                            )}
                        >
                            <div className={cn(
                                "w-8 h-8 rounded-lg flex items-center justify-center transition-colors",
                                active ? "bg-blue-500" : "bg-gray-100 group-hover:bg-gray-200"
                            )}>
                                <Icon size={16} className={active ? "text-white" : "text-gray-500"} />
                            </div>
                            <div>
                                <p className={cn("font-medium leading-tight", active && "text-blue-700")}>{label}</p>
                                <p className="text-[10px] text-gray-400">{sub}</p>
                            </div>
                        </Link>
                    );
                })}
            </nav>

            {/* Footer */}
            <div className="mt-4 px-2 py-3 bg-blue-50 rounded-xl text-center">
                <p className="text-xs text-blue-500 font-medium">4 Cognitive Layers Active</p>
                <p className="text-[10px] text-gray-400 mt-0.5">Reflect · Learn · Grow</p>
            </div>
        </aside>
    );
}
