import os
import pandas as pd

LABELS = {
    "договор": ["договор", "стороны", "предмет договора"],
    "накладная": ["накладная", "поставщик", "получатель"],
    "счет": ["счет-фактура", "оплата", "банковские реквизиты"],
    "приказ": ["приказ", "утверждаю", "на основании"],
    "отчет": ["отчет"],
    "прочее": []
}

def classify_document(text):
    """Определяет тип документа по ключевым словам"""
    for label, keywords in LABELS.items():
        if any(word in text.lower() for word in keywords):
            return label
    return "прочее"

def label_pdfs(txt_folder, output_csv):
    """Размечает все txt-файлы и сохраняет разметку в CSV"""
    data = []

    for filename in os.listdir(txt_folder):
        if filename.endswith(".txt"):
            txt_path = os.path.join(txt_folder, filename)
            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read()
                doc_type = classify_document(text)
                data.append([filename.replace(".txt", ".pdf"), doc_type])

    df = pd.DataFrame(data, columns=["filename", "label"])
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"✅ Разметка сохранена в {output_csv}")

if __name__ == "__main__":
    txt_folder = "parsers/data/pdf"
    output_csv = "parsers/data/labels.csv"
    label_pdfs(txt_folder, output_csv)
