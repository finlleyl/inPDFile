from parsers.parse_pdfs import process_pdf_folder
from parsers.label_pdfs import label_pdfs

PDF_FOLDER = "parsers/data/pdf"
CSV_OUTPUT = "parsers/data/labels.csv"

if __name__ == "__main__":
    print("📌 Начинаем обработку PDF...")
    process_pdf_folder(PDF_FOLDER)

    print("\n📌 Начинаем разметку документов...")
    label_pdfs(PDF_FOLDER, CSV_OUTPUT)

    print("\n✅ Готово! Все документы обработаны и размечены.")
