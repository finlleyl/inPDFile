import { createContext, useState, useEffect } from "react";
import axios from "axios";

interface AuthContextType {
    username: string | null;
    setUsername: React.Dispatch<React.SetStateAction<string | null>>;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children } : { children: React.ReactNode}) => {
    const [username, setUsername] = useState<string | null>(null);

    useEffect (() => {
        axios.get('http://localhost:8000/auth/me', {
            withCredentials: true
        }).then((response) => {
            setUsername(response.data.email);
            console.log(response);
        }).catch(() => {
            setUsername(null);
        });
    }, []);

    return <AuthContext.Provider value={{ username, setUsername}}>
        { children }
    </AuthContext.Provider>
}