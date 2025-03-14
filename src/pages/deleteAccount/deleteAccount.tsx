import React from 'react';
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext.tsx";
import { useContext } from "react";
import './deleteAccount.css';
import axios from "axios";


const deleteAccount: React.FC = () => {
    const navigate = useNavigate();
    const authContext = useContext(AuthContext);
    if (!authContext) {
        return null;
    }
    const { setUsername }=authContext;


    const handleDelete = async (event: React.FormEvent) => {
        event.preventDefault();

        await axios.delete('http://localhost:8000/auth/delete', {
            withCredentials: true
        }).then((response) => {
            setUsername(null);
            console.log(response);
            navigate('/');
        }).catch((e) => {
            console.error(e);
        })
    };

    return (
        <div className="auth-container">
            <div className="dashboard">
                <h1>Вы точно хотите удалить аккаунт?</h1>
                <p>Это действие необратимо!</p>
                <button onClick={handleDelete}>Удалить</button>
            </div>
        </div>
    );
};

export default deleteAccount;
