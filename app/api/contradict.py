from fastapi import APIRouter
from pydantic import BaseModel
import requests

from app.rag.vector_store import collection

router = APIRouter()


class ContradictRequest(BaseModel):
    document_1: str
    document_2: str
    topic: str


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:8b"


@router.post("/contradict")
def contradict(request: ContradictRequest):

    doc1_results = collection.get(
        where={"source": request.document_1}
    )

    doc2_results = collection.get(
        where={"source": request.document_2}
    )

    doc1_text = "\n\n".join(doc1_results["documents"][:5])
    doc2_text = "\n\n".join(doc2_results["documents"][:5])

    prompt = f"""
You are a contradiction detection assistant.

Topic:
{request.topic}

Document 1:
{doc1_text}

Document 2:
{doc2_text}

Determine:

1. Whether the documents conflict regarding the topic.
2. Explain your reasoning.
3. Quote evidence from both documents.

Respond ONLY in JSON format:

{{
    "conflict": true or false,
    "reasoning": "...",
    "evidence": [
        {{
            "document": "...",
            "snippet": "..."
        }}
    ]
}}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]