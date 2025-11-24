from src.index.index_builder import build_index
from src.index.searcher import search_index

def test_search():
    docs = ["apple banana orange", "car bus train"]
    index, chunks = build_index(docs, index_dir="faiss_index_test2")

    result = search_index("apple", index, chunks, k=1)

    assert len(result) == 1
    assert "apple" in result[0]
