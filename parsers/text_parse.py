import os
import io
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from pdfminer.high_level import extract_text
from PIL import Image


def extract_text_from_pdf(pdf_path):
    try:
        full_text = extract_text(pdf_path).strip()

        if full_text:
            return full_text

        doc = fitz.open(pdf_path)
        for page in doc:
            text = page.get_text("text").strip()
            if text:
                full_text += f"\n{text}"

        if full_text.strip():
            return full_text

        ocr_text = extract_text_with_ocr(pdf_path)
        return ocr_text if ocr_text.strip() else None

    except Exception as e:
        print(f"Ошибка при обработке {pdf_path}: {e}")
        return None


def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    ocr_text = ""

    for img in images:
        text = pytesseract.image_to_string(img, lang="rus")
        ocr_text += f"\n{text}"

    return ocr_text.strip()


def process_pdf_folder(pdf_folder):
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            text = extract_text_from_pdf(pdf_path)

            if text:
                txt_path = pdf_path.replace(".pdf", ".txt")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Обработан: {filename}")
            else:
                print(f"Не удалось извлечь текст из: {filename}")


if __name__ == "__main__":
    pdf_folder = "parsers/data/pdf"
    process_pdf_folder(pdf_folder)
