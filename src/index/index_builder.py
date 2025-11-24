import os
import json
import numpy as np
import faiss
from src.index.chunker import chunk_text
from src.embeddings.embedder import get_embedding

def build_index(documents, index_dir="faiss_index"):
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)

    # Step 1: Convert docs to chunks
    chunks = []
    for doc in documents:
        chunks.extend(chunk_text(doc))

    # Step 2: Embeddings
    vectors = []
    for chunk in chunks:
        vectors.append(get_embedding(chunk))

    vectors = np.array(vectors).astype("float32")

    # Step 3: Build FAISS index
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    # Step 4: Save files
    faiss.write_index(index, f"{index_dir}/index.bin")

    with open(f"{index_dir}/meta.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f)

    return index, chunks
