import React from 'react';
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext.tsx";
import { useContext } from "react";
import './profile.css';
import axios from "axios";


const profile: React.FC = () => {
    const navigate = useNavigate();
    const authContext = useContext(AuthContext);
    if (!authContext) {
        return null;
    }
    const { setUsername }=authContext;
    const { username }=authContext;


    const handleLogout = async (event: React.FormEvent) => {
        event.preventDefault();

        await axios.post('http://localhost:8000/auth/logout', {}, {
            withCredentials: true
        }).then((response) => {
            setUsername(null);
            console.log(response);
            navigate('/authPage');
        }).catch((e) => {
            console.error(e);
        })
    };

    return (
        <div className="auth-container">
            <div className="dashboard">
                <h1>Личный кабинет</h1>
                <p>Добро пожаловать, { username }!</p>
                <button onClick={handleLogout}>Выйти</button>
                <button onClick={() => { navigate('/deleteAccount') }}>Удалить аккаунт</button>
            </div>
        </div>
    );
};

export default profile;
