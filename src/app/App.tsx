import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import { AuthProvider } from "../context/AuthContext";

import {Bounce, ToastContainer} from "react-toastify";
import 'react-toastify/dist/ReactToastify.css'
import 'nprogress/nprogress.css';
import './App.css';

import Header from '../components/header/header';
import Home from '../pages/home/home.tsx';
import History from '../pages/history/history.tsx';
import AuthPage from '../pages/authPage/authPage.tsx';
import ConfirmCode from '../pages/confirmCode/confirmCode';
import Profile from '../pages/profile/profile';
import DeleteAccount from "../pages/deleteAccount/deleteAccount.tsx";

function App() {


  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Header />
          <ToastContainer
            position="bottom-right"
            autoClose={5000}
            hideProgressBar={false}
            newestOnTop={false}
            closeOnClick={false}
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
            theme="light"
            transition={Bounce}
          />
          <div className="main-container">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/history" element={<History />} />
              <Route path="/AuthPage" element={<AuthPage />} />
              <Route path="/confirmCode" element={<ConfirmCode />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/deleteAccount" element={<DeleteAccount />} />
            </Routes>
          </div>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
