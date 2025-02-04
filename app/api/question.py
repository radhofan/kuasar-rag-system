from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional
import shutil
import os
from app.ingestion.extractor import extract_text  
from app.core.prompt import generate_answer_from_ollama  
from app.ingestion.embedding import store_file_chroma 

router = APIRouter()

SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "uploads")
os.makedirs(SAVE_DIR, exist_ok=True)

@router.post("/")
async def ask_question(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None),  
):
    print(f"Received question: {question}")
    print(f"Received file: {file.filename if file else 'No file provided'}")

    if file:
        file_path = os.path.join(SAVE_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = await extract_text(file_path)
        if not extracted_text:
            raise HTTPException(status_code=400, detail="Could not extract text from document")
        
        document_id = store_file_chroma(extracted_text, file.filename)
        if not document_id:
            raise HTTPException(status_code=500, detail="Failed to generate or store embedding")
    else:
        document_id = None

    answer = generate_answer_from_ollama(document_id, question)

    return {
        "answer": answer,
        "document_id": document_id,
    }
