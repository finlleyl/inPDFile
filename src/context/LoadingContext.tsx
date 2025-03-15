import { createContext, useContext, useState } from "react";

interface LoadingContextType {
    loading: boolean;
    progress: number;
    startLoading: () => void;
    stopLoading: () => void;
}

const LoadingContext = createContext<LoadingContextType | null>(null);

export const LoadingProvider = ({ children } : { children: React.ReactNode }) => {
    const [progress, setProgress] = useState<number>(0);
    const [loading, setLoading] = useState<boolean>(false);

    const startLoading = () => {
        setProgress(0);
        setLoading(true);
    };

    const stopLoading = () => {
        setTimeout(() => setProgress(100), 500);
        setLoading(false);
    };

    return (
        <LoadingContext.Provider value={{ loading, progress, startLoading, stopLoading }}>
            { children }
        </LoadingContext.Provider>
    );
}

export const useLoading = () => {
    const context = useContext(LoadingContext);
    if (!context) {
        throw new Error("Используйте useLoading внутри LoadingProvider");
    }
    return context;
};