import pytest
from db.chroma import get_collection, reset_collection


@pytest.fixture(autouse=True)
def cleanup():
    yield
    try:
        reset_collection()
    except Exception:
        pass


def test_get_collection_returns_collection():
    coll = get_collection()
    assert coll.name == "embedded_docs"


def test_add_and_query():
    coll = get_collection()
    coll.add(
        ids=["doc1_chunk0"],
        documents=["GPIO BSRR寄存器用于设置和复位引脚。"],
        embeddings=[[0.1] * 768],
        metadatas=[{"filename": "test.pdf", "page": 12, "chunk_index": 0}],
    )
    results = coll.query(query_embeddings=[[0.1] * 768], n_results=1)
    assert len(results["ids"][0]) == 1
    assert "BSRR" in results["documents"][0][0]


def test_query_empty_collection():
    reset_collection()
    coll = get_collection()
    results = coll.query(query_embeddings=[[0.5] * 768], n_results=3)
    assert len(results["ids"][0]) == 0
