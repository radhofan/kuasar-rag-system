from fastapi import FastAPI
from app.api.endpoints import document, question, answer

app = FastAPI(title="RAG System API")

# Include API routes
app.include_router(document.router, prefix="/document", tags=["Document"])
app.include_router(question.router, prefix="/question", tags=["Question"])
app.include_router(answer.router, prefix="/answer", tags=["Answer"])

# Root call
@app.get("/")
def root():
    return {"message": "RAG System API is running"}

# Optional: Startup and Shutdown events
@app.on_event("startup")
def startup():
    print("Starting up...")  # Initialize ChromaDB if needed

@app.on_event("shutdown")
def shutdown():
    print("Shutting down...")  # Cleanup resources if needed
