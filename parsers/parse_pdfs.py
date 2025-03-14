import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Selenium settings
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

BASE_URL = "https://mai.ru/common/documents/reports/"
SAVE_FOLDER = "data/pdf"
os.makedirs(SAVE_FOLDER, exist_ok=True)

def download_pdf(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Скачан: {save_path}")
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")

def parse_pdfs_selenium():
    driver.get(BASE_URL)
    time.sleep(2)

    pdf_links = []
    elements = driver.find_elements(By.TAG_NAME, "a")
    for element in elements:
        link = element.get_attribute("href")
        if link and link.endswith(".pdf"):
            pdf_links.append(link)

    for pdf_url in pdf_links:
        pdf_name = os.path.join(SAVE_FOLDER, os.path.basename(pdf_url))
        download_pdf(pdf_url, pdf_name)

    driver.quit()

if __name__ == "__main__":
    parse_pdfs_selenium() 
