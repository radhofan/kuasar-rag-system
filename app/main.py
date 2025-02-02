from fastapi import FastAPI
from app.api.endpoints import document, answer
from app.api import question

app = FastAPI(title="RAG System API")

# Root call
@app.get("/")
def root():
    return {"message": "RAG System API is running"}

# Optional: Startup and Shutdown events
@app.on_event("startup")
def startup():
    print("Starting up...") 

@app.on_event("shutdown")
def shutdown():
    print("Shutting down...")  

# Question
app.include_router(question.router, prefix="/question", tags=["Question"]) # Ask Question
