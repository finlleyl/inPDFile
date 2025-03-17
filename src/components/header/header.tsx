import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from "../../context/AuthContext";
import styles from '../header/header.module.css';
// @ts-ignore
import Logo from '../../assets/file-contract-svgrepo-com.svg?react';

const header: React.FC = () => {
  const navigate = useNavigate();
  const authContext = useContext(AuthContext);
  if (!authContext) {
    return null;
  }
  const { username }=authContext;


  return (
    <header className={styles.header}>
      <div className={styles.logoContainer}>
        <Link to="/" className={styles.logoLink}>
          <Logo />
        </Link>
        <div className={styles.naiming}>
          <h1>inPDFile</h1>
        </div>
      </div>
      <nav className={styles.nav}>
        <ul>
          <li>
            <Link to="/">Главная</Link>
          </li>
          <li>
            <Link to="/history">История загрузок</Link>
          </li>
          <li>
            {username ? (
                <button onClick={() => navigate("/profile")}>{ username }</button>
            ) : (
                <button className="login-button" onClick={() => navigate("/authPage")}>Войти</button>
            )}

          </li>
        </ul>
      </nav>
    </header>
  );
};

export default header;
