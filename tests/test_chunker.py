from src.index.chunker import chunk_text

def test_chunking():
    text = "a" * 2000
    chunks = chunk_text(text, chunk_size=800)
    assert len(chunks) == 3
