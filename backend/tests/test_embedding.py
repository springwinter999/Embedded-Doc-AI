import pytest
from services.embedding import embed_text, embed_batch
from unittest.mock import patch, MagicMock


@patch("services.embedding.httpx.Client")
def test_embed_text_returns_vector(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": [{"embedding": [0.1] * 768}]
    }
    mock_response.raise_for_status = MagicMock()
    mock_client.return_value.__enter__.return_value.post.return_value = mock_response

    result = embed_text("GPIO配置")
    assert len(result) == 768
    assert isinstance(result, list)


@patch("services.embedding.httpx.Client")
def test_embed_batch_returns_vectors(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": [
            {"embedding": [0.1] * 768},
            {"embedding": [0.2] * 768},
        ]
    }
    mock_response.raise_for_status = MagicMock()
    mock_client.return_value.__enter__.return_value.post.return_value = mock_response

    results = embed_batch(["文本A", "文本B"])
    assert len(results) == 2
    assert len(results[0]) == 768


def test_embed_text_empty_input():
    with pytest.raises(ValueError):
        embed_text("")
