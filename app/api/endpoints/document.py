from fastapi import APIRouter

router = APIRouter()

@router.get("/md")
def ask_question(query: str):
    return {"question": query, "answer": "This is a placeholder answer."}

@router.get("/pdf")
def ask_question(query: str):
    return {"question": query, "answer": "This is a placeholder answer."}