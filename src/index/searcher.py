import numpy as np
from src.embeddings.embedder import get_embedding

def search_index(query: str, index, chunks, k=3):
    if not chunks or index is None:
        return []

    q_vec = np.array([get_embedding(query)], dtype="float32")

    distances, indices = index.search(q_vec, k)
    return [chunks[i] for i in indices[0]]
