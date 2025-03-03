import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

def extract_text_from_pdf(pdf_path):
    """Извлекает текст из PDF, используя PyMuPDF и OCR"""
    try:
        doc = fitz.open(pdf_path)
        full_text = ""

        for page in doc:
            text = page.get_text("text")
            if text.strip():
                full_text += f"\n{text}"
            else:
                # Если текста нет, используем OCR
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes("ppm")))
                text = pytesseract.image_to_string(img, lang="rus")
                full_text += f"\n{text}"

        return full_text.strip()
    except Exception as e:
        print(f"Ошибка при чтении {pdf_path}: {e}")
        return None

def process_pdf_folder(pdf_folder):
    """Обрабатывает все PDF в папке и сохраняет текст в файлы .txt"""
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            text = extract_text_from_pdf(pdf_path)

            if text:
                txt_path = pdf_path.replace(".pdf", ".txt")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"✅ Обработан: {filename}")

if __name__ == "__main__":
    pdf_folder = "parsers/data/pdf"
    process_pdf_folder(pdf_folder)
