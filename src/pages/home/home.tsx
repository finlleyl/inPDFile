import React, { useState } from 'react';
import { useLoading } from "../../context/LoadingContext";
import './home.css';
import axios from "axios";

const home: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const { startLoading, stopLoading } = useLoading();


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

    const formData = new FormData();
    formData.append("file", file);

    startLoading();
    setLoading(true);

    // Эта функция просто для тестирования. Имитируем задержку, пока отправляется файл.
    await new Promise(resolve => setTimeout(resolve, 2000));

    await axios.post("http://localhost:8000/pdf/upload", formData, {
        withCredentials: true,
        headers: { "Content-Type": "multipart/form-data" },
    }).then(response => {
      setFile(null);
      console.log("Файл загружен:", response.data);
    }).catch (e => {
      console.error(e);
    }).finally(() => {
      stopLoading();
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
