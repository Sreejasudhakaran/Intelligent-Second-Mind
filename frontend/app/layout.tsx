import type { Metadata } from "next";
import "./globals.css";
import Providers from "./providers";
import Sidebar from "@/components/ui/Sidebar";

export const metadata: Metadata = {
    title: "JARVIS – Decision Intelligence",
    description: "AI-powered personal decision management system with 4 cognitive layers.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <head>
                <link rel="preconnect" href="https://fonts.googleapis.com" />
                <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
            </head>
            <body className="bg-gradient-to-br from-[#EEF4FF] to-[#F8FAFF] min-h-screen">
                <Providers>
                    <div className="flex min-h-screen">
                        <Sidebar />
                        <main className="flex-1 ml-64 p-8 min-h-screen">
                            {children}
                        </main>
                    </div>
                </Providers>
            </body>
        </html>
    );
}
