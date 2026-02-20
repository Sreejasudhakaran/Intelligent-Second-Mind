"use client";

import { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { Mic, MicOff } from "lucide-react";

interface VoiceButtonProps {
    onTranscript: (text: string) => void;
}

declare global {
    interface Window {
        webkitSpeechRecognition: new () => SpeechRecognition;
        SpeechRecognition: new () => SpeechRecognition;
    }
}

export default function VoiceButton({ onTranscript }: VoiceButtonProps) {
    const [isRecording, setIsRecording] = useState(false);
    const [isSupported, setIsSupported] = useState(false);
    const recognitionRef = useRef<SpeechRecognition | null>(null);

    useEffect(() => {
        if (typeof window !== "undefined") {
            const SpeechRecognition =
                window.SpeechRecognition || window.webkitSpeechRecognition;
            setIsSupported(!!SpeechRecognition);
        }
    }, []);

    const startRecording = () => {
        const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = "en-US";

        recognition.onresult = (event: SpeechRecognitionEvent) => {
            const transcript = Array.from(event.results)
                .map((r) => r[0].transcript)
                .join(" ");
            onTranscript(transcript);
        };

        recognition.onerror = () => setIsRecording(false);
        recognition.onend = () => setIsRecording(false);

        recognition.start();
        recognitionRef.current = recognition;
        setIsRecording(true);
    };

    const stopRecording = () => {
        recognitionRef.current?.stop();
        setIsRecording(false);
    };

    if (!isSupported) return null;

    return (
        <motion.button
            type="button"
            whileHover={{ scale: 1.08 }}
            whileTap={{ scale: 0.95 }}
            onClick={isRecording ? stopRecording : startRecording}
            className={`w-12 h-12 rounded-full flex items-center justify-center transition-all duration-200 ${isRecording
                    ? "bg-red-500 text-white mic-recording shadow-lg"
                    : "bg-blue-500 text-white hover:bg-blue-600 shadow-blue-glow"
                }`}
            title={isRecording ? "Stop recording" : "Start voice input"}
        >
            {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
        </motion.button>
    );
}
