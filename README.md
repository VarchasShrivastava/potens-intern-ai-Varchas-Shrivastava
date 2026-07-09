Potens Document RAG System
Multilingual Citation-Aware Retrieval Augmented Generation (RAG) with Contradiction Detection

Overview

This project is a document-grounded Retrieval Augmented Generation (RAG) system built as part of the Potens AI Internship Assignment (Q1: Document Q&A with Citations).

The system ingests documents, converts them into semantic embeddings, stores them in a vector database, and answers user questions strictly using retrieved evidence from the uploaded documents.

Unlike conventional chatbots, the system is designed to:

Provide source-backed answers
Include citations and evidence snippets
Explicitly refuse to answer when the information is not present in the documents
Detect contradictions between documents
Support multilingual interactions
Assignment Requirements Coverage
Requirement	Implementation
Ingest, chunk, embed and store documents	✅ Implemented
Explain chunking strategy in README	✅ Implemented
/ask endpoint with citations	✅ Implemented
Citation contains file, page/chunk and snippet	✅ Implemented
/contradict endpoint	✅ Implemented
Multilingual support	✅ Implemented
Streamlit UI	✅ Implemented
No silent hallucination	✅ Implemented
Free/open-source LLM	✅ Qwen3 via Ollama
Vector Store	✅ ChromaDB
Features
Document Ingestion Pipeline
PDF Upload API
Text extraction using PyPDF
Metadata preservation
Automatic indexing into ChromaDB
Citation-Aware Question Answering

Every answer contains:

Source document
Page number
Chunk identifier
Supporting snippet

Example:

{
  "answer": "Employees are entitled to 20 days of annual leave per year.",
  "citations": [
    {
      "source_file": "employee_policy.pdf",
      "page": 4,
      "chunk_id": "employee_policy.pdf_p4_c1",
      "snippet": "Employees are entitled to twenty days of annual leave annually."
    }
  ]
}
Contradiction Detection

The system compares two uploaded documents on a specific topic and determines whether they conflict.

Example:

Input:

{
  "document_1": "policy_v1.pdf",
  "document_2": "policy_v2.pdf",
  "topic": "remote work policy"
}

Output:

{
  "conflict": true,
  "reasoning": "Document 1 allows hybrid work while Document 2 mandates full office attendance.",
  "evidence": [
    {
      "document": "policy_v1.pdf",
      "snippet": "Employees may work remotely up to three days per week."
    },
    {
      "document": "policy_v2.pdf",
      "snippet": "Employees are expected to attend the office five days per week."
    }
  ]
}
Hallucination Prevention

A primary design goal of this system is to prevent unsupported responses.

The model receives the following instructions:

Answer strictly from retrieved context.
Never use external knowledge.
Explicitly state when information is unavailable.

If the uploaded documents do not contain the answer, the system returns:

The provided documents do not contain enough information to answer this question.

This ensures the system remains document-grounded and auditable.

System Architecture
                    ┌─────────────────┐
                    │ Uploaded PDFs   │
                    └────────┬────────┘
                             │
                             ▼
                  ┌──────────────────┐
                  │ PDF Text Loader  │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Document Chunker │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Embedding Model  │
                  │ BGE Small v1.5   │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │    ChromaDB      │
                  │  Vector Store    │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Semantic Search  │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Qwen3 via Ollama │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Answer + Citation│
                  └──────────────────┘
Chunking Strategy

The assignment explicitly requires explanation of chunking strategy.

The system uses Recursive Character Text Splitting with the following configuration:

Parameter	Value
Chunk Size	2000 characters
Chunk Overlap	200 characters
Split Priority	Paragraph → Line → Sentence → Word

Configuration:

RecursiveCharacterTextSplitter(
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
Why This Strategy?
Large chunks preserve semantic context

Smaller chunks often fragment concepts across multiple embeddings.

Overlap prevents information loss

Information located near chunk boundaries remains retrievable.

Hierarchical splitting maintains readability

Paragraphs and sentences remain intact whenever possible.

Metadata Preservation

Every chunk stores metadata required for citation generation.

Example:

{
  "chunk_id": "policy.pdf_p3_c2",
  "source": "policy.pdf",
  "page": 3
}

This allows the system to generate traceable and explainable answers.

Technology Stack
Layer	Technology
API Backend	FastAPI
Frontend UI	Streamlit
Vector Database	ChromaDB
Embeddings	BAAI/bge-small-en-v1.5
LLM	Qwen3 via Ollama
Document Parsing	PyPDF
Retrieval	Dense Vector Similarity Search
API Endpoints
Upload Documents
POST /upload

Uploads and indexes PDF documents.

Ask Questions
POST /ask

Request:

{
  "question": "What is the leave policy?"
}
Contradiction Detection
POST /contradict

Request:

{
  "document_1": "policy_v1.pdf",
  "document_2": "policy_v2.pdf",
  "topic": "remote work policy"
}
Health Check
GET /health
Streamlit UI

The application includes a Streamlit interface that allows users to:

Upload documents
Ask questions
View citations
Compare documents for contradictions
Project Structure
potens-intern-ai-varchas-shrivastava/
│
├── app/
│   ├── api/
│   │   ├── upload.py
│   │   ├── ask.py
│   │   └── contradict.py
│   │
│   └── rag/
│       ├── loader.py
│       ├── chunker.py
│       ├── vector_store.py
│       ├── retriever.py
│       └── generator.py
│
├── ui/
│   └── app.py
│
├── main.py
├── requirements.txt
└── README.md
Running Locally
Clone Repository
git clone https://github.com/<username>/potens-intern-ai-Varchas-Shrivastava.git
cd potens-intern-ai-Varchas-Shrivastava
Create Virtual Environment
python -m venv venv
Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Install Ollama

Install Ollama and pull the model:

ollama pull qwen3:8b
Start Backend
uvicorn main:app --reload
Start Streamlit UI
streamlit run ui/app.py
Limitations
OCR support for scanned PDFs is currently not implemented.
Contradiction detection quality depends on document coverage and retrieval quality.
Multilingual support currently relies on the multilingual capabilities of Qwen3.
Future Improvements
Confidence scoring
Reranking layer
OCR support
Hybrid retrieval (BM25 + Dense Search)
Human-in-the-loop verification
Docker deployment
Conclusion

This project demonstrates a production-style RAG architecture with:

Grounded generation
Explainability
Auditable citations
Contradiction detection
Multilingual capabilities

The system prioritizes trustworthiness and traceability over generative freedom, making it suitable for document-heavy domains such as enterprise policy search, legal document analysis, research assistance, and internal knowledge management systems.

Ai tools used- Copilot, Codex, Chatgpt, Claude
