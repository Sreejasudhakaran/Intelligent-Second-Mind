import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./constants/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        blue: {
          DEFAULT: "#3B82F6",
          50: "#EFF6FF",
          100: "#DBEAFE",
          200: "#BFDBFE",
          300: "#93C5FD",
          400: "#60A5FA",
          500: "#3B82F6",
          600: "#2563EB",
          700: "#1D4ED8",
        },
        green: {
          DEFAULT: "#22C55E",
          50: "#F0FDF4",
          100: "#DCFCE7",
          200: "#BBF7D0",
          500: "#22C55E",
          600: "#16A34A",
        },
        orange: {
          DEFAULT: "#F59E0B",
          50: "#FFFBEB",
          100: "#FEF3C7",
          400: "#FBBF24",
          500: "#F59E0B",
        },
        slate: {
          700: "#334155",
          800: "#1E293B",
          900: "#0F172A",
        },
      },
      backgroundImage: {
        "jarvis-gradient": "linear-gradient(135deg, #EEF4FF 0%, #F8FAFF 100%)",
      },
      boxShadow: {
        card: "0 2px 16px rgba(0, 0, 0, 0.06)",
        "card-hover": "0 8px 30px rgba(0, 0, 0, 0.10)",
        "blue-glow": "0 4px 20px rgba(59, 130, 246, 0.35)",
      },
      borderRadius: {
        "2xl": "16px",
        "3xl": "24px",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
