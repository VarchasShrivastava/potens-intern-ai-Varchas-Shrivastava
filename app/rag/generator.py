import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:8b"


def generate_answer(question, context_chunks):
    context = "\n\n".join(
        [
            f"[Source: {chunk['source']} Page: {chunk['page']}]\n{chunk['text']}"
            for chunk in context_chunks
        ]
    )

    prompt = f"""
You are a document-grounded assistant.

Rules:
1. Answer ONLY using provided context.
2. Never use outside knowledge.
3. If information is missing, explicitly say so.
4. Respond in the same language as the question.
5. Include citations where possible.

Context:
{context}

Question:
{question}

Answer:
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