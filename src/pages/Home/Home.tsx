import React, { useState } from 'react';
import './Home.css'; // Импорт стилей

const Home: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [analysisResult, setAnalysisResult] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleFileUpload = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/analyze-pdf', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setAnalysisResult(result.message);
      } else {
        setAnalysisResult('Ошибка при анализе файла');
      }
    } catch (error) {
      setAnalysisResult('Ошибка при отправке файла');
    } finally {
      setLoading(false);
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
        <button onClick={handleFileUpload} disabled={!file || loading}>
          {loading ? 'Загрузка...' : 'Загрузить файл'}
        </button>
      </div>
      {analysisResult && (
        <div className="analysis-result">
          <h3>Результат анализа:</h3>
          <p>{analysisResult}</p>
        </div>
      )}
    </main>
  );
};

export default Home;
