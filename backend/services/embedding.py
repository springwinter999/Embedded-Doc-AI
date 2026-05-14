from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from config import EMBEDDING_MODEL

_model: SentenceTransformer | None = None
EMBED_BATCH_SIZE = 32


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
    """Convert multiple texts to embedding vectors in sub-batches to avoid OOM on CPU."""
    if not texts:
        return []
    model = _get_model()
    all_embeddings = []
    for i in tqdm(range(0, len(texts), EMBED_BATCH_SIZE), desc="Embedding"):
        batch = texts[i:i + EMBED_BATCH_SIZE]
        embeddings = model.encode(batch, normalize_embeddings=True)
        all_embeddings.extend(embeddings.tolist())
    return all_embeddings
