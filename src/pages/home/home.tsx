import React, { useState } from 'react';
import './home.css';
import axios from "axios";
import {toast} from "react-toastify";
import NProgress from 'nprogress';
import Footer from './Footer';

const home: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  };

  const handleFileUpload= async () => {
    if (!file) {
      toast.error("Выберите файл!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);
    NProgress.start();

    await axios.post("http://localhost:8000/pdf/upload", formData, {
          onUploadProgress: (progressEvent) => {
            if (!progressEvent.total) return;
            const percentage = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            NProgress.set(percentage);
            console.log('progress loading: ' + percentage);
          },
          withCredentials: true,
          headers: { "Content-Type": "multipart/form-data" },

    }).then(response => {
      toast.success('Файл загружен');
      setFile(null);
      console.log("Файл загружен:", response.data);

    }).catch (e => {
      setFile(null);
      toast.error('Ошибка загрузки');
      console.error(e);

    }).finally(() => {
      NProgress.done;
      setLoading(false);
    })
  };

  return (
    <main className="home-container">
      <div>
        <h1>Добро пожаловать на сайт анализа PDF-документов!</h1>
        <p>Загрузите ваш PDF-файл для анализа.</p>
      </div>
      <div className="file-upload-container">
        <label htmlFor="file-upload" className="custom-file-upload">
          Выберите PDF-файл
        </label>
        <input
          id="file-upload"
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <button onClick={handleFileUpload} disabled={!file || loading}>
          {loading ? 'Загрузка...' : 'Загрузить файл'}
        </button>
      </div>

      <Footer /> {/* футер*/}


    </main>



  );
};

export default home;
