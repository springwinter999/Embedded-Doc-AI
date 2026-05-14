from db.chroma import get_collection, reset_collection
from services.embedding import embed_text, embed_batch
from config import TOP_K_RESULTS


def add_chunks(chunks: list[dict]):
    """Index a list of {text, metadata} chunks into ChromaDB."""
    if not chunks:
        return
    coll = get_collection()
    texts = [c["text"] for c in chunks]
    embeddings = embed_batch(texts)
    ids = [c["metadata"]["chunk_id"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    batch_size = 50
    for i in range(0, len(ids), batch_size):
        coll.add(
            ids=ids[i:i + batch_size],
            documents=texts[i:i + batch_size],
            embeddings=embeddings[i:i + batch_size],
            metadatas=metadatas[i:i + batch_size],
        )


def search(query: str, top_k: int = TOP_K_RESULTS) -> list[dict]:
    """Search ChromaDB for chunks semantically similar to query."""
    coll = get_collection()
    query_embedding = embed_text(query)
    results = coll.query(query_embeddings=[query_embedding], n_results=top_k)

    items = []
    if results["ids"] and results["ids"][0]:
        for i in range(len(results["ids"][0])):
            items.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i] if results["documents"] else "",
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else None,
            })
    return items


def get_document_stats() -> list[dict]:
    """Return indexed document names and their chunk counts."""
    coll = get_collection()
    results = coll.get()
    if not results["ids"]:
        return []
    stats = {}
    for meta in results["metadatas"]:
        fname = meta.get("filename", "unknown")
        stats[fname] = stats.get(fname, 0) + 1
    return [{"filename": k, "chunk_count": v} for k, v in stats.items()]


def delete_document(filename: str) -> int:
    """Delete all chunks belonging to a specific filename. Returns count of removed chunks."""
    coll = get_collection()
    results = coll.get(where={"filename": filename}, include=[])
    ids_to_delete = results["ids"]
    if ids_to_delete:
        coll.delete(ids=ids_to_delete)
    return len(ids_to_delete)


def clear_all():
    """Remove all documents from the collection."""
    reset_collection()
