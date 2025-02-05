from fastapi import FastAPI
from app.api import question
from app.stats import stats
from starlette.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="RAG System API")
app.mount("/static", StaticFiles(directory=Path.cwd() / 'static'), name="static")

# Root call
@app.get("/")
def root():
    return {"message": "RAG System API is running"}

app.include_router(question.router, prefix="/question", tags=["Question"]) 
app.include_router(stats.router, prefix="/logs", tags=["Logs"]) 
