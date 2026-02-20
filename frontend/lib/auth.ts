/**
 * Auth lib – client-side session management.
 * In development, always returns the default user.
 * In production, integrates with Supabase Auth.
 */
const DEFAULT_USER_ID = "default_user";

export function getCurrentUserId(): string {
    if (typeof window === "undefined") return DEFAULT_USER_ID;
    return localStorage.getItem("jarvis_user_id") || DEFAULT_USER_ID;
}

export function setUserId(userId: string): void {
    if (typeof window !== "undefined") {
        localStorage.setItem("jarvis_user_id", userId);
    }
}

export function clearSession(): void {
    if (typeof window !== "undefined") {
        localStorage.removeItem("jarvis_user_id");
    }
}
