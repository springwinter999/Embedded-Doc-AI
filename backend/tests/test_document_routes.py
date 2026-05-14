from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


@patch("routers.document.vector_store.get_document_stats")
def test_list_documents_empty(mock_stats):
    mock_stats.return_value = []
    response = client.get("/api/documents")
    assert response.status_code == 200
    assert response.json() == {"documents": []}


@patch("routers.document.vector_store.get_document_stats")
def test_list_documents_with_data(mock_stats):
    mock_stats.return_value = [
        {"filename": "test.pdf", "chunk_count": 42}
    ]
    response = client.get("/api/documents")
    assert response.status_code == 200
    data = response.json()
    assert len(data["documents"]) == 1
    assert data["documents"][0]["chunk_count"] == 42


@patch("routers.document.vector_store.clear_all")
@patch("routers.document.vector_store.add_chunks")
@patch("routers.document.parser.parse_pdf")
def test_index_documents(mock_parse, mock_add, mock_clear):
    mock_parse.return_value = [
        {"text": "chunk1", "metadata": {"filename": "test.pdf", "page": 1, "chunk_index": 0, "chunk_id": "id0"}}
    ]
    response = client.post("/api/documents/index")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["files_processed"] >= 0
