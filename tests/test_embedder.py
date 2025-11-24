from src.embeddings.embedder import get_embedding

def test_embedding_output():
    embedding = get_embedding("hello world")
    assert isinstance(embedding, list)
    assert len(embedding) > 100  # should be ~768+
