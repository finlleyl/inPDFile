import React from 'react';
import { Link } from 'react-router-dom';
import styles from '../header/header.module.css';
import Logo from '../../assets/file-contract-svgrepo-com.svg?react';

const Header: React.FC = () => {
  return (
    <header className={styles.header}>
      <div className={styles.logoContainer}>
        <Link to="/" className={styles.logoLink}>
          <Logo />
        </Link>
        <div className={styles.naiming}>
          <h1>inPDFile</h1>
          <p>мгновенное определение типа документа</p>
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
            <Link to="/AuthPage">Профиль</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
