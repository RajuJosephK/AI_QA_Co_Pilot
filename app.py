import streamlit as st
import os
from docx import Document

from src.loader import load_all_documents
from src.readers.pdf_reader import read_pdf
from src.readers.docx_reader import read_docx
from src.readers.txt_reader import read_txt
from src.readers.pptx_reader import read_pptx
from src.readers.html_reader import read_html
from src.readers.excel_reader import read_xlsx

import streamlit as st
import os
import json
import numpy as np
from dotenv import load_dotenv
from src.loader import load_all_documents
from src.index.index_builder import build_index
from src.index.index_loader import load_index
from src.index.searcher import search_index

from src.embeddings.embedder import get_embedding, client

# --------------------------------------
# Config
# --------------------------------------
INDEX_DIR = "faiss_index"
DOC_FOLDER = "sample_docs"
CHUNK_SIZE = 800
TOP_K = 3

os.makedirs(INDEX_DIR, exist_ok=True)

# --------------------------------------
# Load existing FAISS index at startup
# --------------------------------------
index, chunks = load_index(INDEX_DIR)
if index is None:
    index = None
    chunks = []

# --------------------------------------
# Streamlit UI
# --------------------------------------
st.title("AI QA Co-Pilot (RAG-powered Testing Knowledge Assistant)")
st.write("Upload documents, rebuild index, and ask questions using your own knowledge base.")

# ======================================================
# 🔄 BUTTON: REBUILD FAISS INDEX FROM EXISTING FOLDER
# ======================================================
if st.button("🔄 Rebuild Index from Existing Files"):
    with st.spinner("Reading documents & rebuilding index..."):
        # Load documents from folder
        docs = load_all_documents(DOC_FOLDER)

        # Rebuild index using your existing clean builder
        index, chunks = build_index(docs, index_dir=INDEX_DIR)

    st.success(f"Rebuilt index using all documents from '{DOC_FOLDER}'.")

# ======================================================
# 📂 Upload NEW documents
# ======================================================
st.subheader("📤 Upload New Documents")
uploaded_files = st.file_uploader(
    "Upload PDF, DOCX, or TXT files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    new_docs = []

    # Read uploaded files using your reader modules
    for file in uploaded_files:
        if file.type == "application/pdf":
            new_docs.append(load_pdf(file))
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            new_docs.append(load_docx(file))
        elif file.type == "text/plain":
            new_docs.append(load_txt(file))

    if new_docs:
        st.info("Indexing new documents...")
        # Merge with existing data (new docs + old chunks)
        # 1. Combine new docs with existing doc chunks → build new full index
        merged_docs = new_docs + chunks

        # Rebuild index using your core function
        index, chunks = build_index(merged_docs, INDEX_DIR)

        st.success(f"Uploaded {len(uploaded_files)} files and updated the FAISS index.")

# ======================================================
# 🤖 LLM Model selection
# ======================================================
model_option = st.selectbox(
    "Choose LLM Model",
    ["openai/gpt-oss-20b", "google/gemma-3-4b-it:free"]
)

# ======================================================
# ❓ Chat section
# ======================================================
question = st.text_input("Ask a question:")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("Ask") and question:
    if index is None or not chunks:
        st.warning("No indexed documents found. Please upload or rebuild index.")
    else:
        # Retrieve relevant chunks
        context_chunks = search_index(question, index, chunks, k=TOP_K)
        context_text = "\n".join(context_chunks)

        # Call LLM
        response = client.chat.completions.create(
            model=model_option,
            messages=[
                {"role": "system", "content": "Answer only using the provided context."},
                {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion:\n{question}"}
            ]
        )

        answer = response.choices[0].message.content
        st.session_state.chat_history.append((question, answer))

# ======================================================
# 💬 Chat History
# ======================================================
st.subheader("💬 Chat History")

for i, (q, a) in enumerate(st.session_state.chat_history[::-1]):
    st.markdown(f"**Q{i+1}: {q}**")
    st.markdown(f"{a}")
