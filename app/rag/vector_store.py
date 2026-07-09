from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

client = PersistentClient(path="data/chroma")

collection = client.get_or_create_collection(
    name="documents"
)

embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def store_chunks(chunks):
    documents = []
    embeddings = []
    metadatas = []
    ids = []

    for chunk in chunks:
        documents.append(chunk["text"])
        embeddings.append(
            embedding_model.encode(chunk["text"]).tolist()
        )

        metadatas.append({
            "source": chunk["source"],
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"]
        })

        ids.append(chunk["chunk_id"])

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )