import React, { useState } from 'react';
import './home.css';
import axios from "axios";
import { toast } from "react-toastify";
import NProgress from 'nprogress';
import Footer from './Footer';

const Home: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [dragActive, setDragActive] = useState<boolean>(false);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setFile(event.target.files[0]);
        }
    };

    const handleFileUpload = async () => {
        if (!file) {
            toast.error("Выберите файл!");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        setLoading(true);
        NProgress.start();

        try {
            const response = await axios.post("http://localhost:8000/pdf/upload", formData, {
                onUploadProgress: (progressEvent) => {
                    if (!progressEvent.total) return;
                    const percentage = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    NProgress.set(percentage);
                    console.log('progress loading: ' + percentage);
                },
                withCredentials: true,
                headers: { "Content-Type": "multipart/form-data" },
            });

            toast.success('Файл загружен');
            setFile(null);
            console.log("Файл загружен:", response.data);
        } catch (e) {
            toast.error('Ошибка загрузки');
            console.error(e);
        } finally {
            NProgress.done();
            setLoading(false);
        }
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
        <div className="page-container">
            <main className="content">

                <div className="info-section">
                    <div className="info-box">
                        <p>Документы окружают нас повсюду - договоры, чеки, соглашения. Важно быстро определить их тип, будь то в работе или повседневной жизни.</p>
                    </div>
                    <div className="info-box">
                        <p>Наш сервис бесплатно определяет тип документа в PDF-файле за секунды. Просто загрузите файл - и получите результат без лишних усилий.</p>
                    </div>
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

                    <button className="upload-button" onClick={handleFileUpload} disabled={!file || loading}>
                        {loading ? 'Загрузка...' : 'Загрузить'}
                    </button>
                </div>
            </main>
            <Footer />
        </div>

    );
};

export default Home;
