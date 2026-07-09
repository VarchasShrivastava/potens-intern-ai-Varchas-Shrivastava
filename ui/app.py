import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Potens Document RAG",
    layout="wide"
)

st.title("📄 Potens Document RAG")
st.write("Multilingual citation-aware document assistant")

tab1, tab2 = st.tabs(["Ask Questions", "Contradiction Detection"])

# ==========================
# Upload Section
# ==========================

st.sidebar.header("Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }

        response = requests.post(
            f"{API_URL}/upload",
            files=files
        )

        if response.status_code == 200:
            st.sidebar.success(
                f"Uploaded {uploaded_file.name}"
            )

# ==========================
# Ask Tab
# ==========================

with tab1:

    question = st.text_input(
        "Ask a question about uploaded documents"
    )

    if st.button("Ask") and question:

        response = requests.post(
            f"{API_URL}/ask",
            json={
                "question": question
            }
        )

        result = response.json()

        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Citations")

        for citation in result["citations"]:
            with st.expander(
                f"{citation['source_file']} | Page {citation['page']}"
            ):
                st.write(
                    f"Chunk ID: {citation['chunk_id']}"
                )

                st.write(
                    citation["snippet"]
                )

# ==========================
# Contradiction Tab
# ==========================

with tab2:

    doc1 = st.text_input(
        "Document 1 filename"
    )

    doc2 = st.text_input(
        "Document 2 filename"
    )

    topic = st.text_input(
        "Topic to compare"
    )

    if st.button("Check Contradiction"):

        response = requests.post(
            f"{API_URL}/contradict",
            json={
                "document_1": doc1,
                "document_2": doc2,
                "topic": topic
            }
        )

        st.subheader("Result")

        st.write(
            response.json()
        )