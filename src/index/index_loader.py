import os
import faiss
import json

def load_index(index_dir="faiss_index"):
    index_file = f"{index_dir}/index.bin"
    meta_file = f"{index_dir}/meta.json"

    if not os.path.exists(index_file) or not os.path.exists(meta_file):
        return None, []

    index = faiss.read_index(index_file)

    with open(meta_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    return index, chunks
