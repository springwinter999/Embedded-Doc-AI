import httpx
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, EMBEDDING_MODEL


def embed_text(text: str) -> list[float]:
    """Convert a single text to a 768-dim embedding vector."""
    if not text or not text.strip():
        raise ValueError("Input text must not be empty")
    embeddings = embed_batch([text])
    return embeddings[0]


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Convert multiple texts to embedding vectors in one API call."""
    with httpx.Client(timeout=60) as client:
        response = client.post(
            f"{DEEPSEEK_BASE_URL}/v1/embeddings",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": EMBEDDING_MODEL,
                "input": texts,
            },
        )
        response.raise_for_status()
        data = response.json()
        return [item["embedding"] for item in data["data"]]
