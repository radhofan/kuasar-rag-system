from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import shutil
import os
import time
import uuid
from app.ingestion.extractor import extract_text  
from app.core.prompt import generate_answer_from_ollama  
from app.ingestion.embedding import store_file_chroma 
from app.stats.stats import log_request  

router = APIRouter()

SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(SAVE_DIR, exist_ok=True)

@router.post("/")
async def ask_question(  
    question: str = Form(""),  
    file: Optional[UploadFile] = File(None),  
):
    print(f"Received question: {question}")
    print(f"Received file: {file.filename if file else 'No file provided'}")

    if not question and not file:  
        raise HTTPException(status_code=400, detail="Either a question or a file must be provided.")

    request_id = str(uuid.uuid4())  
    start_time = time.time()

    try:
        document_id = None

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
            
            os.remove(file_path)

        if question:  
            answer, token_usage = generate_answer_from_ollama(document_id, question)  
            response_time = time.time() - start_time
            log_request(request_id, token_usage, response_time, "SUCCESS")
            return {"answer": answer}

        return {"document_id": document_id}  

    except Exception as e:
        response_time = time.time() - start_time
        log_request(request_id, 0, response_time, "FAILURE")  
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")
