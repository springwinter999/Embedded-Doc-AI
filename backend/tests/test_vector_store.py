import pytest
from services.vector_store import add_chunks, search, get_document_stats, clear_all
from db.chroma import reset_collection
from unittest.mock import patch


@pytest.fixture(autouse=True)
def cleanup():
    yield
    try:
        reset_collection()
    except Exception:
        pass


@patch("services.vector_store.embed_text")
@patch("services.vector_store.embed_batch")
def test_add_and_search(mock_embed_batch, mock_embed_text):
    mock_embed_batch.return_value = [[0.1] * 768, [0.2] * 768]
    mock_embed_text.return_value = [0.15] * 768

    chunks = [
        {"text": "GPIO BSRR寄存器用于设置引脚", "metadata": {"filename": "test.pdf", "page": 10, "chunk_index": 0, "chunk_id": "id0"}},
        {"text": "UART波特率通过USART_BRR配置", "metadata": {"filename": "test.pdf", "page": 20, "chunk_index": 0, "chunk_id": "id1"}},
    ]
    add_chunks(chunks)

    stats = get_document_stats()
    assert len(stats) == 1
    assert stats[0]["filename"] == "test.pdf"
    assert stats[0]["chunk_count"] == 2

    results = search("GPIO怎么配置")
    assert len(results) > 0
