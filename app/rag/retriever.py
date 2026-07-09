from app.rag.vector_store import (
    collection,
    embedding_model
)


def retrieve(query, top_k=5):
    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_chunks = []

    for document, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        retrieved_chunks.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "chunk_id": metadata["chunk_id"]
        })

    return retrieved_chunks