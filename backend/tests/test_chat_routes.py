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
def test_post_chat_new_conversation(mock_search, mock_ask):
    mock_search.return_value = [
        {
            "id": "doc_p1_c0",
            "text": "GPIO BSRR寄存器用于置位和复位引脚",
            "metadata": {"filename": "test.pdf", "page": 12},
            "distance": 0.15,
        }
    ]
    mock_ask.return_value = "使用 HAL_GPIO_TogglePin 函数翻转引脚电平。"

    response = client.post("/api/chat", json={
        "question": "怎么让PB7引脚上的LED闪烁？",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["answer"]
    assert data["conversation_id"]
    assert len(data["sources"]) >= 1
    assert data["sources"][0]["page"] == 12


@patch("routers.chat.llm.ask")
@patch("routers.chat.vector_store.search")
def test_post_chat_existing_conversation(mock_search, mock_ask):
    mock_search.return_value = []
    mock_ask.return_value = "文档中未找到相关信息。"

    resp1 = client.post("/api/chat", json={"question": "Q1"})
    conv_id = resp1.json()["conversation_id"]

    resp2 = client.post("/api/chat", json={
        "question": "Q2",
        "conversation_id": conv_id,
    })
    assert resp2.status_code == 200
    assert resp2.json()["conversation_id"] == conv_id


def test_get_chat_history_not_found():
    response = client.get("/api/chat/nonexistent")
    assert response.status_code == 404


@patch("routers.chat.llm.ask")
@patch("routers.chat.vector_store.search")
def test_get_chat_history(mock_search, mock_ask):
    mock_search.return_value = []
    mock_ask.return_value = "GPIO配置方法..."

    resp = client.post("/api/chat", json={"question": "GPIO配置？"})
    conv_id = resp.json()["conversation_id"]

    response = client.get(f"/api/chat/{conv_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == conv_id
    assert len(data["messages"]) >= 2
