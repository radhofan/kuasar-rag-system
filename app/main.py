from fastapi import FastAPI
from app.api import question
from app.stats import stats

app = FastAPI(title="RAG System API")

# Root call
@app.get("/")
def root():
    return {"message": "RAG System API is running"}

app.include_router(question.router, prefix="/question", tags=["Question"]) 
app.include_router(stats.router, prefix="/logs", tags=["Logs"]) 
