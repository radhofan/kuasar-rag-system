from fastapi import APIRouter

router = APIRouter()

@router.get("/ask")
def ask_question(query: str):
    return {"question": query, "answer": "This is a placeholder answer."}
