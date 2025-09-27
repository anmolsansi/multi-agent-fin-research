# models/embedder.py
from sentence_transformers import SentenceTransformer

_model = None


def get_embedder():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model


def embed_texts(texts):
    return get_embedder().encode(texts, show_progress_bar=False, normalize_embeddings=True).tolist()
