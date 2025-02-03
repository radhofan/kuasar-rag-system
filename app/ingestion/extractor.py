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
    """
    Clean the extracted text by removing unnecessary metadata, HTML tags, markdown syntax, special characters, and line breaks.
    """
    # Decode any HTML-encoded characters to ensure they don't get processed incorrectly
    text = html.unescape(text)

    # Use BeautifulSoup to remove HTML tags
    soup = BeautifulSoup(text, 'html.parser')
    clean_text = soup.get_text()

    # Remove any unnecessary markdown syntax (e.g., * for italics, # for headers)
    clean_text = re.sub(r"[#*`-]", "", clean_text)

    # Remove any leftover HTML-like entities
    clean_text = re.sub(r"<.*?>", "", clean_text)

    # Remove any unnecessary line breaks and extra spaces, tabs, and newlines
    clean_text = ' '.join(clean_text.split())

    # Remove extra line breaks or paragraph breaks, making sure it remains a one-liner
    clean_text = re.sub(r'\n+', ' ', clean_text)  # Replace multiple line breaks with a single space
    clean_text = re.sub(r'\s+', ' ', clean_text)  # Replace multiple spaces with a single space

    return clean_text.strip()  # Optionally remove leading/trailing whitespace

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
