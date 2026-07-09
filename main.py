from fastapi import FastAPI

from app.api.upload import router as upload_router
from app.api.ask import router as ask_router

app = FastAPI(
    title="Potens Document RAG",
    version="1.0.0",
    description="Multilingual citation-aware RAG system with contradiction detection."
)

# Register API routes
app.include_router(upload_router)
app.include_router(ask_router)


@app.get("/")
def root():
    return {
        "message": "Potens Document RAG API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }