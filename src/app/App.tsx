import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
//import React from 'react';
import './App.css';
import Header from '../components/header/header';
import Home from '../pages/Home/Home';
import History from '../pages/History';
import AuthPage from '../pages/AuthPage/AuthPage';
import ConfirmCode from '../pages/confirmCode/confirmCode';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <div className="main-container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/history" element={<History />} />
            <Route path="/AuthPage" element={<AuthPage />} />
            <Route path="/confirmCode" element={<ConfirmCode />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
