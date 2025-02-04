import fitz  
import os
from bs4 import BeautifulSoup
import re
import html

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()  
        return clean_text(text)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def extract_text_from_md(md_path: str) -> str:
    try:
        with open(md_path, 'r', encoding='utf-8') as file:
            text = file.read()
            return clean_text(text)
    except Exception as e:
        print(f"Error extracting text from MD: {e}")
        return None

def clean_text(text: str) -> str:
    text = html.unescape(text)
    soup = BeautifulSoup(text, 'html.parser')
    clean_text = soup.get_text()
    clean_text = re.sub(r"[#*`-]", "", clean_text)
    clean_text = re.sub(r"<.*?>", "", clean_text)
    clean_text = ' '.join(clean_text.split())

    clean_text = re.sub(r'\n+', ' ', clean_text) 
    clean_text = re.sub(r'\s+', ' ', clean_text)  

    return clean_text.strip()  

async def extract_text(file_path: str) -> str:
    try:
        ext = os.path.splitext(file_path)[1].lower()  
        
        if ext == ".pdf":
            return extract_text_from_pdf(file_path)
        elif ext == ".md":
            return extract_text_from_md(file_path)
        else:
            raise ValueError("Unsupported file type. Please upload a PDF or Markdown file.")
    
    except Exception as e:
        print(f"Error processing the file: {e}")
        return None
