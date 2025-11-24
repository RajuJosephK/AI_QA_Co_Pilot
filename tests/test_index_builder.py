from src.index.index_builder import build_index

def test_build_index():
    docs = ["This is a test document." * 50]
    index, chunks = build_index(docs, index_dir="faiss_index_test")

    assert index.ntotal == len(chunks)
    assert len(chunks) > 1
