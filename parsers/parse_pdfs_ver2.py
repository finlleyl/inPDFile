import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = "https://obrazec-dogovora.ru/other"
SAVE_FOLDER = "data/pdf_other_types"
os.makedirs(SAVE_FOLDER, exist_ok=True)

visited_urls = set()
MAX_DEPTH = 1000  

def get_html(url):
    """Получает HTML-код страницы, если это не бинарный файл"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        return None  
    
    return response.text

def find_pdfs(url):
    """Находит и скачивает PDF файлы со страницы"""
    html = get_html(url)
    if not html:
        return
    
    soup = BeautifulSoup(html, "html.parser")
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(url, href)
        
        if full_url.endswith(".pdf"):
            download_pdf(full_url)

def download_pdf(url):
    """Скачивает PDF файл"""
    pdf_name = os.path.join(SAVE_FOLDER, os.path.basename(urlparse(url).path))
    
    if os.path.exists(pdf_name):
        print(f"✅ Уже скачан: {pdf_name}")
        return
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(pdf_name, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"✅ Скачан: {pdf_name}")
    except Exception as e:
        print(f"❌ Ошибка при скачивании {url}: {e}")

def crawl(url, depth=0):
    """Рекурсивный обход сайта, ограниченный глубиной"""
    if depth > MAX_DEPTH or url in visited_urls:
        return
    
    print(f"🔍 Обхожу страницу: {url}")
    visited_urls.add(url)
    find_pdfs(url)
    
    html = get_html(url)
    if not html:
        return
    
    soup = BeautifulSoup(html, "html.parser")
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(url, href)
        
        if full_url.startswith(BASE_URL) and full_url not in visited_urls:
            crawl(full_url, depth + 1)

if __name__ == "__main__":
    crawl(BASE_URL) 
