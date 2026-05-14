import chromadb
from chromadb.config import Settings
from config import CHROMA_PERSIST_DIR
from typing import Optional

_client = None


def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False),
        )
    return _client


def get_collection() -> chromadb.Collection:
    client = get_client()
    return client.get_or_create_collection(
        name="embedded_docs",
        metadata={"hnsw:space": "cosine"},
    )


def reset_collection():
    global _client
    try:
        client = get_client()
        client.delete_collection("embedded_docs")
    except Exception:
        pass
    _client = None
