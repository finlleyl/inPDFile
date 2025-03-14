import React, { useState } from 'react';
import './home.css';
import axios from "axios";

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
      alert("Выберите файл!");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    await axios.post("http://localhost:8000/pdf/upload", formData, {
        withCredentials: true,
        headers: { "Content-Type": "multipart/form-data" },
    }).then(response => {
      console.log("Файл загружен:", response.data);
    }).catch (e => {
      console.error(e);
    }).finally(() => {
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
    </main>
  );
};

export default home;
