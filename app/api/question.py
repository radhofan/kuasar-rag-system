from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import shutil
import os
from app.ingestion.extractor import extract_text  # Function to extract text
from app.core.prompt import generate_answer_from_ollama  # Import your function to generate the answer
from app.ingestion.embedding import generate_embedding_with_ollama  # Import to generate embedding initially

router = APIRouter()

SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "uploads")
os.makedirs(SAVE_DIR, exist_ok=True)

@router.post("/")
async def ask_question(
    file: UploadFile = File(...), 
    question: str = Form(...),
):
    # Save uploaded file
    file_path = os.path.join(SAVE_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from the document
    extracted_text = await extract_text(file_path)
    if not extracted_text:
        raise HTTPException(status_code=400, detail="Could not extract text from document")
    
    # Store the embedding and get the document_id (file name here)
    document_id = generate_embedding_with_ollama(extracted_text, file.filename)

    if not document_id:
        raise HTTPException(status_code=500, detail="Failed to generate or store embedding")

    # Now, generate the answer using the document_id and question
    answer = generate_answer_from_ollama(document_id, question)

    # Return the answer
    return {
        "answer": answer,
        "document_id": document_id,
    }
