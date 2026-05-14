import pytest
from services.llm import build_prompt, ask
from unittest.mock import patch, MagicMock


def test_build_prompt_includes_context_and_question():
    context = [
        {"text": "GPIO BSRR寄存器用于置位和复位", "metadata": {"page": 12, "filename": "test.pdf"}},
        {"text": "ODR寄存器可读可写", "metadata": {"page": 14, "filename": "test.pdf"}},
    ]
    question = "如何翻转GPIO引脚？"
    messages = build_prompt(question, context)

    assert len(messages) >= 2
    assert messages[0]["role"] == "system"
    assert "寄存器" in messages[0]["content"]
    assert messages[1]["role"] == "user"
    assert question in messages[1]["content"]
    assert "BSRR" in messages[0]["content"] or "BSRR" in messages[1]["content"]


def test_build_prompt_empty_context():
    question = "如何翻转GPIO？"
    messages = build_prompt(question, [])
    assert len(messages) >= 2
    assert "没有找到" in messages[0]["content"]


@patch("services.llm.httpx.Client")
def test_ask_returns_answer(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "使用HAL_GPIO_TogglePin函数。\n\n来源: test.pdf §12.3"}}]
    }
    mock_response.raise_for_status = MagicMock()
    mock_client.return_value.__enter__.return_value.post.return_value = mock_response

    result = ask([
        {"role": "system", "content": "你是嵌入式专家"},
        {"role": "user", "content": "如何翻转GPIO？"},
    ])
    assert "HAL_GPIO_TogglePin" in result
