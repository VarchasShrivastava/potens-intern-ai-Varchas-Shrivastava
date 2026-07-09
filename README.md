Potens Document RAG System

A multilingual, citation-aware Retrieval Augmented Generation (RAG) system built using FastAPI, ChromaDB, Sentence Transformers, Ollama and Streamlit.

The system allows users to upload documents, ask questions grounded in those documents, detect contradictions between documents, and receive answers with citations and supporting evidence.

Features
Document upload through API and UI
PDF text extraction
Semantic chunking with metadata preservation
Vector embeddings using Sentence Transformers
ChromaDB vector storage
Grounded question answering
Source citations with:
source file
page number
chunk identifier
evidence snippet
Contradiction detection between documents
Multilingual query support
Streamlit UI
Hallucination prevention
Architecture
User Uploads PDF
        ↓
PDF Loader
        ↓
Text Extraction
        ↓
Chunking
        ↓
Embeddings
        ↓
ChromaDB Vector Store
        ↓
Retriever
        ↓
Qwen3 via Ollama
        ↓
Answer + Citations
Tech Stack
Component	Technology
API	FastAPI
UI	Streamlit
Vector Database	ChromaDB
Embeddings	Sentence Transformers
LLM	Qwen3 via Ollama
Document Processing	PyPDF
Retrieval	Dense Vector Search
Chunking Strategy

The system uses a RecursiveCharacterTextSplitter with:

Chunk Size: 2000 characters
Chunk Overlap: 200 characters

Metadata is preserved for every chunk:

{
    "chunk_id": "policy.pdf_p3_c2",
    "source": "policy.pdf",
    "page": 3
}

This enables precise citations and evidence tracking.

The separator hierarchy is:

Double newline
Single newline
Sentence boundary
Whitespace
Character boundary

This preserves semantic coherence while minimizing context fragmentation.

Hallucination Prevention

The model is explicitly instructed to:

answer only from retrieved context
avoid external knowledge
state when information is unavailable

If documents do not contain the answer, the system returns:

The provided documents do not contain enough information to answer this question.
API Endpoints
Upload Documents
POST /upload

Uploads and stores documents for indexing.

Ask Questions
POST /ask

Example request:

{
    "question": "What is the leave policy?"
}

Example response:

{
    "answer": "Employees are entitled to 20 days of annual leave.",
    "citations": [
        {
            "source_file": "employee_policy.pdf",
            "page": 4,
            "chunk_id": "employee_policy.pdf_p4_c1",
            "snippet": "Employees are entitled to 20 days..."
        }
    ]
}
Contradiction Detection
POST /contradict

Example request:

{
    "document_1": "policy_v1.pdf",
    "document_2": "policy_v2.pdf",
    "topic": "remote work policy"
}

Example response:

{
    "conflict": true,
    "reasoning": "Document 1 allows hybrid work while Document 2 requires office attendance.",
    "evidence": [...]
}
Running Locally
Clone Repository
git clone <repository-url>
cd potens-document-rag
Create Environment
python -m venv venv

Activate:

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
Start UI
streamlit run ui/app.py
Project Structure
project/
│
├── app/
│   ├── api/
│   └── rag/
│
├── data/
│   ├── uploads/
│   └── chroma/
│
├── ui/
│
├── tests/
│
├── README.md
├── requirements.txt
└── main.py
Future Improvements
Confidence scoring
Reranking layer
OCR support for scanned PDFs
Hybrid search (BM25 + dense retrieval)
Human-in-the-loop verification
Docker deployment