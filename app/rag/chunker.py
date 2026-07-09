from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


def chunk_documents(documents):
    chunks = []

    for document in documents:
        text_chunks = splitter.split_text(document["text"])

        for idx, chunk in enumerate(text_chunks):
            chunks.append({
                "chunk_id": f"{document['source']}_p{document['page']}_c{idx}",
                "source": document["source"],
                "page": document["page"],
                "text": chunk
            })

    return chunks