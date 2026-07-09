from fastapi import FastAPI

from app.api.upload import router as upload_router
from app.api.ask import router as ask_router
from app.api.contradict import router as contradict_router

app = FastAPI(
    title="Potens Document RAG",
    description="Multilingual citation-aware RAG system with contradiction detection",
    version="1.0.0"
)

# Register API routes
app.include_router(upload_router)
app.include_router(ask_router)
app.include_router(contradict_router)


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