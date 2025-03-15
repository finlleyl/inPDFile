import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext.tsx";
import { useContext } from "react";
import './authPage.css';
import axios from "axios";

const authPage: React.FC = () => {
  const navigate = useNavigate();
  const authContext = useContext(AuthContext);
  if (!authContext) {
    return null;
  }
  const { setUsername }=authContext;

  const [isLogin, setIsLogin] = useState<boolean>(true);
  const [user, setUser] = useState<string>('');           // username
  const [password, setPassword] = useState<string>('');   // password

  const handleAuth = async (event: React.FormEvent) => {
    event.preventDefault();

    if (user && password) {
      if (isLogin) {
        await axios
            .post('http://localhost:8000/auth/login', {
              "email": user,
              "password": password,
            }, {
              withCredentials: true
        })
            .then(function (response) {
              setUsername(user);
              console.log(response);
              navigate('/profile');
        })
            .catch(e => {
              console.error(e);
        })

      } else {
        await axios.post('http://localhost:8000/auth/register', {
          "email": user,
          "password": password,
        }, {
          withCredentials: true
        }).then(response => {
          setUsername(user);
          console.log(response);
          navigate('/confirmCode', { state : { user }});
        }).catch(e => {
          console.error(e);
        })
      }
    }
  };

  return (
    <div className="auth-container">
      <h1>{isLogin ? 'Вход' : 'Регистрация'}</h1>
      <form className="auth-form" onSubmit={handleAuth}>
        <div>
          <label htmlFor="username">Имя пользователя:</label>
          <input
            type="text"
            id="username"
            value={user}
            onChange={(e) => setUser(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Пароль:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">
          {isLogin ? 'Войти' : 'Зарегистрироваться'}
        </button>
      </form>
      <button className="toggle-button" onClick={() => setIsLogin(!isLogin)}>
        {isLogin
          ? 'Нет аккаунта? Зарегистрируйтесь'
          : 'Уже есть аккаунт? Войдите'}
      </button>
    </div>
  );
};

export default authPage;
