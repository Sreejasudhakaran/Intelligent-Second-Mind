"use client";

import { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { Mic, MicOff, AlertCircle } from "lucide-react";

interface VoiceRecorderProps {
    onTranscript: (text: string) => void;
    className?: string;
    /** compact = small inline mic icon next to a field label */
    compact?: boolean;
}

declare global {
    interface Window {
        SpeechRecognition: new () => SpeechRecognition;
        webkitSpeechRecognition: new () => SpeechRecognition;
    }
}

export default function VoiceRecorder({ onTranscript, className = "", compact = false }: VoiceRecorderProps) {
    const [isRecording, setIsRecording] = useState(false);
    const [isSupported, setIsSupported] = useState(false);
    const [liveText, setLiveText] = useState("");
    const recognitionRef = useRef<SpeechRecognition | null>(null);

    useEffect(() => {
        if (typeof window !== "undefined") {
            const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
            setIsSupported(!!SR);
        }
    }, []);

    const startRecording = () => {
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SR();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US";

        recognition.onresult = (event: SpeechRecognitionEvent) => {
            let interim = "";
            let final = "";
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const result = event.results[i];
                if (result.isFinal) {
                    final += result[0].transcript;
                } else {
                    interim += result[0].transcript;
                }
            }
            setLiveText(interim);
            if (final) {
                onTranscript(final);
                setLiveText("");
            }
        };

        recognition.onerror = () => {
            setIsRecording(false);
            setLiveText("");
        };
        recognition.onend = () => {
            setIsRecording(false);
            setLiveText("");
        };

        recognition.start();
        recognitionRef.current = recognition;
        setIsRecording(true);
    };

    const stopRecording = () => {
        recognitionRef.current?.stop();
        setIsRecording(false);
        setLiveText("");
    };

    if (!isSupported) {
        return compact ? null : (
            <div className={`flex items-center gap-2 text-xs text-gray-400 ${className}`}>
                <AlertCircle size={14} />
                Voice input not supported in this browser
            </div>
        );
    }

    // ── Compact inline mic (for field labels) ─────────────────────────────────
    if (compact) {
        return (
            <span className={`inline-flex items-center gap-1.5 ${className}`}>
                <motion.button
                    type="button"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={isRecording ? stopRecording : startRecording}
                    title={isRecording ? "Stop recording" : "Speak to fill this field"}
                    className={`w-6 h-6 rounded-full flex items-center justify-center transition-all duration-200 shadow-sm ${isRecording
                            ? "bg-red-500 text-white animate-pulse"
                            : "bg-blue-100 text-blue-500 hover:bg-blue-500 hover:text-white"
                        }`}
                >
                    {isRecording ? <MicOff size={11} /> : <Mic size={11} />}
                </motion.button>
                {isRecording && (
                    <span className="text-[10px] text-red-400 italic animate-pulse">
                        {liveText ? `"${liveText.slice(0, 30)}…"` : "Listening…"}
                    </span>
                )}
            </span>
        );
    }

    // ── Full-size mic (for Decision Title) ────────────────────────────────────
    return (
        <div className={`flex flex-col items-center gap-2 ${className}`}>
            <motion.button
                type="button"
                whileHover={{ scale: 1.06 }}
                whileTap={{ scale: 0.94 }}
                onClick={isRecording ? stopRecording : startRecording}
                className={`w-12 h-12 rounded-full flex items-center justify-center transition-all duration-200 shadow-md ${isRecording
                        ? "bg-red-500 text-white mic-recording"
                        : "bg-blue-500 text-white hover:bg-blue-600 shadow-blue-glow"
                    }`}
                title={isRecording ? "Stop recording" : "Start voice input"}
            >
                {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
            </motion.button>
            {isRecording && liveText && (
                <p className="text-xs text-gray-400 italic max-w-[200px] text-center truncate">
                    &ldquo;{liveText}&rdquo;
                </p>
            )}
            <p className="text-xs text-gray-400">
                {isRecording ? "Listening… click to stop" : "Voice input"}
            </p>
        </div>
    );
}
