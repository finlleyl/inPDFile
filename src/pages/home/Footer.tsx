import React from 'react';
import './Footer.css';

const Footer: React.FC = () => {
    return (
        <footer className="footer">
            <div className="footer-container">
                <div className="footer-info">
                    <h3><strong>inPDFFile - ваш помощник в работе с документами</strong></h3>
                    <p>
                        В современном мире обработка документов требует скорости и точности.
                        inPDFFile помогает автоматически определять тип PDF-файлов, экономя ваше
                        время и снижая вероятность ошибок. Будь то чеки, договоры, соглашения
                        или другие документы - наш сервис обеспечит вам мгновенный результат.
                    </p>
                </div>
                <div className="footer-contacts">
                    <h3>Контакты:</h3>
                    <p>Если у вас есть вопросы или предложения, свяжитесь с нами:</p>
                    <p>Email: <a href="mailto:support@inpdfile.com">support@inpdfile.com</a></p>
                    <p>Адрес: адрес</p>
                    <p>Социальные сети: <a href="#">Telegram</a> | <a href="#">X</a> | <a href="#">LinkedIn</a></p>
                    <p>2025 inPDFFile. Все права защищены. &copy;</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;