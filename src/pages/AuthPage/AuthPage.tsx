import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import './AuthPage.css';
import axios from "axios";

const AuthPage: React.FC = () => {
  const [isLogin, setIsLogin] = useState<boolean>(true);
  const [username, setUsername] = useState<string>('');                  // username
  const [password, setPassword] = useState<string>('');                  // password
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const navigate = useNavigate();



  // Auth - авторизация, отслеживание отправки формы
  const handleAuth = async (event: React.FormEvent) => {
    event.preventDefault();

    if (username && password) {
      if (isLogin) {
        axios
            .post('http://localhost:8000/auth/login', {
          "email": username,
          "password": password,
        }, {
          withCredentials: true
        })
            .then(function (response) {
          console.log(response);
            setIsAuthenticated(true);
        })
            .catch(e => {
          console.error(e);
        })

      } else {
        axios
            .post('http://localhost:8000/auth/register', {
          "email": username,
          "password": password,
        }, {
          withCredentials: true
        })
            .then(response => {
          console.log(response);
          navigate('/confirmCode', { state : { username }});
        })
            .catch(e => {
          console.error(e);
        })
      }
    }
  };

  // logout - сброс данных
  const handleLogout = () => {
    setIsAuthenticated(false);
    setUsername('');
    setPassword('');
  };

  if (isAuthenticated) {
    return (
      <div className="auth-container">
        <div className="dashboard">
          <h1>Личный кабинет</h1>
          <p>Добро пожаловать, {username}!</p>
          <button onClick={handleLogout}>Выйти</button>
        </div>
      </div>
    );
  }


  return (
    <div className="auth-container">
      <h1>{isLogin ? 'Вход' : 'Регистрация'}</h1>
      <form className="auth-form" onSubmit={handleAuth}>
        <div>
          <label htmlFor="username">Имя пользователя:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
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

export default AuthPage;
