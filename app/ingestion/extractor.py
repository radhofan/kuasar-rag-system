import fitz  
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()  
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def extract_text_from_md(md_path: str) -> str:
    try:
        with open(md_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error extracting text from MD: {e}")
        return None

async def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()  
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".md":
        return extract_text_from_md(file_path)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or Markdown file.")
