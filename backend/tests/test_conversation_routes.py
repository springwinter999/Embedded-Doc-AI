import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from db.sqlite import init_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    init_db(":memory:")


@patch("routers.chat.llm.ask")
@patch("routers.chat.vector_store.search")
def test_list_conversations(mock_search, mock_ask):
    mock_search.return_value = []
    mock_ask.return_value = "answer"

    client.post("/api/chat", json={"question": "GPIO配置？"})
    response = client.get("/api/conversations")
    assert response.status_code == 200
    data = response.json()
    assert len(data["conversations"]) >= 1
    assert "title" in data["conversations"][0]
    assert "id" in data["conversations"][0]


@patch("routers.chat.llm.ask")
@patch("routers.chat.vector_store.search")
def test_delete_conversation(mock_search, mock_ask):
    mock_search.return_value = []
    mock_ask.return_value = "answer"

    resp = client.post("/api/chat", json={"question": "测试问题"})
    conv_id = resp.json()["conversation_id"]

    response = client.delete(f"/api/conversations/{conv_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"

    list_resp = client.get("/api/conversations")
    ids = [c["id"] for c in list_resp.json()["conversations"]]
    assert conv_id not in ids


def test_delete_nonexistent():
    response = client.delete("/api/conversations/nonexistent")
    assert response.status_code == 404
