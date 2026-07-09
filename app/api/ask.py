from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.retriever import retrieve
from app.rag.generator import generate_answer

router = APIRouter()


class AskRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_question(request: AskRequest):

    chunks = retrieve(
        request.question,
        top_k=5
    )

    if len(chunks) == 0:
        return {
            "answer": "The provided documents do not contain enough information to answer this question.",
            "citations": []
        }

    answer = generate_answer(
        request.question,
        chunks
    )

    citations = []

    for chunk in chunks:
        citations.append({
            "source_file": chunk["source"],
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
            "snippet": chunk["text"][:250]
        })

    return {
        "answer": answer,
        "citations": citations
    }