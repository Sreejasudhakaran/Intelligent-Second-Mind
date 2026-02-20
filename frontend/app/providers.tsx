"use client";

import { useState, createContext, useContext } from "react";

interface UserContextValue {
    userId: string;
    setUserId: (id: string) => void;
}

const UserContext = createContext<UserContextValue>({
    userId: "default_user",
    setUserId: () => { },
});

export function useUser() {
    return useContext(UserContext);
}

export default function Providers({ children }: { children: React.ReactNode }) {
    const [userId, setUserId] = useState("default_user");

    return (
        <UserContext.Provider value={{ userId, setUserId }}>
            {children}
        </UserContext.Provider>
    );
}
