import numpy as np
import pytest
import services.embedding as emb
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def reset_model():
    emb._model = None
    yield


@patch("services.embedding.SentenceTransformer")
def test_embed_text_returns_vector(mock_st):
    mock_model = MagicMock()
    mock_model.encode.return_value = np.array([0.1] * 768, dtype=np.float32)
    mock_st.return_value = mock_model

    result = emb.embed_text("GPIO配置")
    assert len(result) == 768
    assert isinstance(result, list)


@patch("services.embedding.SentenceTransformer")
def test_embed_batch_returns_vectors(mock_st):
    mock_model = MagicMock()
    mock_model.encode.return_value = np.array(
        [[0.1] * 768, [0.2] * 768], dtype=np.float32
    )
    mock_st.return_value = mock_model

    results = emb.embed_batch(["文本A", "文本B"])
    assert len(results) == 2
    assert len(results[0]) == 768


def test_embed_text_empty_input():
    emb._model = None
    with pytest.raises(ValueError):
        emb.embed_text("")
