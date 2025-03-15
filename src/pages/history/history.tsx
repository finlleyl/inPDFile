import React, {useEffect, useState} from 'react';
import './history.css';
import axios from "axios";
import { useLoading } from "../../context/LoadingContext";
import LoadingOrbitBar from "../../components/loadingBar/loadingOrbitBar";

interface FileData {
  file_name: string;
  file_size: string;
  file_path: string;
  status: string;
  classification: string;
  document_type: string;
  upload_date: string;
  has_signature: string;
  has_stamp: string;
}

const history: React.FC = () => {
  const [files, setFiles] = useState<FileData[]>([]);
  const [visibleFiles, setVisibleFiles] = useState<FileData[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const { startLoading, stopLoading } = useLoading();

  useEffect(() => {
    const fetchFiles = async () => {
      setLoading(true);
      startLoading();

      // Эта функция просто для тестирования. Имитируем задержку, пока отправляется файл.
      await new Promise(resolve => setTimeout(resolve, 2000));

      await axios.get<FileData[]>("http://localhost:8000/pdf/history/", {
        withCredentials: true,
      }).then(response => {
        setFiles(response.data);
        setVisibleFiles(response.data.slice(0, 10)); // Показываем первые 10
      }).catch (e => {
        console.error("Ошибка загрузки истории файлов:", e);
      }).finally(() => {
        stopLoading();
        setLoading(false);
      });
    };

    fetchFiles();
  }, []);

  const loadMoreFiles = () => {
    const newIndex = currentIndex + 10;
    setVisibleFiles(files.slice(0, newIndex + 10));
    setCurrentIndex(newIndex);
  };

  return (
      <div className="home-container">
        <h1>История загруженных файлов</h1>
        {loading ? (<LoadingOrbitBar />) : (
            <>
              <ul>
                {visibleFiles.map((file, index) => (
                    <li key={index} style={{ border: "1px solid #ccc", padding: "10px", marginBottom: "10px" }}>
                      <p><strong>{file.file_name}</strong> ({file.file_size})</p>
                      <p><strong>Дата загрузки:</strong> {file.upload_date}</p>
                      <p><strong>Статус:</strong> {file.status}</p>
                      <p><strong>Классификация:</strong> {file.classification}</p>
                      <p><strong>Тип документа:</strong> {file.document_type}</p>
                      <p><strong>Подпись:</strong> {file.has_signature}</p>
                      <p><strong>Печать:</strong> {file.has_stamp}</p>
                    </li>
                ))}
              </ul>
              {visibleFiles.length === 0 && (
                  <p>У вас нет загруженных файлов</p>
              )}
              {visibleFiles.length < files.length && (
                  <button onClick={loadMoreFiles} style={{ marginTop: "10px", padding: "10px" }}>
                    Показать еще
                  </button>
              )}
            </>
        )}
      </div>
  );
};

export default history;
