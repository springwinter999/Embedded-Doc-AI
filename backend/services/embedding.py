from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_text(text: str) -> list[float]:
    """Convert a single text to an embedding vector."""
    if not text or not text.strip():
        raise ValueError("Input text must not be empty")
    model = _get_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Convert multiple texts to embedding vectors."""
    model = _get_model()
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()
