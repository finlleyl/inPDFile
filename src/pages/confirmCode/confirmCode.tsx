import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext.tsx";
import { useContext } from "react";
import './confirmCode.css';
import axios from "axios";


const confirmCode: React.FC = () => {
    const authContext = useContext(AuthContext);
    if (!authContext) {
        return null;
    }
    const { username }=authContext;

    const [code, setCode] = useState<string>('');
    const navigate = useNavigate();

    const handleCode = async (event: React.FormEvent) => {
        event.preventDefault();

        await axios.put(`http://localhost:8000/auth/confirm?code=${code}`, {}, {
            withCredentials : true
        }).then(function (response){
            console.log(response);
                navigate('/');
        }).catch(e => {
            console.error(e);
        })
    }

    return (
    <div className="auth-container">
        <h1>Здравствуйте!</h1>
        <form className="auth-form" onSubmit={handleCode}>
            <h2>Приятно познакомиться, {username}</h2>
            <h2>Мы направили вам четырехзначный код на почту</h2>
            <div>
                <label htmlFor="code">Введите код:</label>
                <input
                    type="code"
                    id="code"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    required
                />
            </div>
            <button type="submit">
                Отправить
            </button>
        </form>
    </div>
    );
};

export default confirmCode;
