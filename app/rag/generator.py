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
1. Answer ONLY using the provided context.
2. Do not use outside knowledge.
3. If the answer is not present in the context, respond with:
   "The provided documents do not contain enough information to answer this question."
4. Mention supporting citations in your answer.

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