import os
import pytest
from services.parser import parse_pdf, chunk_text


def test_chunk_text():
    text = "ABCD " * 600  # ~3000 chars, should produce multiple chunks
    chunks = chunk_text(text, chunk_size=500, overlap=100)
    assert len(chunks) > 1
    for c in chunks:
        assert len(c) <= 500


def test_chunk_text_short():
    text = "Short text"
    chunks = chunk_text(text, chunk_size=1000, overlap=100)
    assert len(chunks) == 1
    assert chunks[0] == text


def test_chunk_overlap():
    text = "0123456789" * 100
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    if len(chunks) >= 2:
        end_of_first = chunks[0][-20:]
        start_of_second = chunks[1][:20]
        assert end_of_first == start_of_second


def test_parse_pdf_returns_list():
    pdf_path = os.path.join(
        os.path.dirname(__file__), "..", "data",
        "UM3132 STM32H5 HAL和低层驱动程序的描述.pdf"
    )
    if os.path.exists(pdf_path):
        chunks = parse_pdf(pdf_path, chunk_size=500, overlap=50)
        assert isinstance(chunks, list)
        assert len(chunks) > 0
        for chunk in chunks:
            assert "text" in chunk
            assert "metadata" in chunk
            assert len(chunk["text"]) <= 500
    else:
        pytest.skip("PDF file not found in data/")
