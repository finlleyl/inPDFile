import React, { useState } from 'react';
import './home.css';
import axios from "axios";
import {toast} from "react-toastify";
import NProgress from 'nprogress';

const home: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [dragActive, setDragActive] = useState<boolean>(false);

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
            const percentage = Math.round((progressEvent.loaded * 100) / progressEvent.total) / 100;
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

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragActive(true);
  };

  const handleDragLeave = () => {
    setDragActive(false);
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragActive(false);
    if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
      setFile(event.dataTransfer.files[0]);
    }
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

        <div
            className={`file-drop-zone ${dragActive ? 'active' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
        >
          <p>Перетащите сюда ваши файлы</p>
        </div>

        {file && <p className="selected-file">Выбран файл: {file.name}</p>}

        <button onClick={handleFileUpload} disabled={!file || loading}>
          {loading ? 'Загрузка...' : 'Загрузить файл'}
        </button>
      </div>
    </main>
  );
};

export default home;
