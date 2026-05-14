import pdfplumber


def extract_text_from_pdf(filepath: str) -> list[dict]:
    """Extract text per page from PDF. Returns list of {page, text}."""
    pages = []
    with pdfplumber.open(filepath) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():
                pages.append({"page": i + 1, "text": text.strip()})
    return pages


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks of at most chunk_size characters."""
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def parse_pdf(filepath: str, chunk_size: int = 1000, overlap: int = 200) -> list[dict]:
    """Parse a PDF into chunked text with metadata. Returns [{text, metadata}]."""
    filename = filepath.replace("\\", "/").split("/")[-1]
    pages = extract_text_from_pdf(filepath)
    result = []
    for page_data in pages:
        chunks = chunk_text(page_data["text"], chunk_size, overlap)
        for ci, chunk in enumerate(chunks):
            result.append({
                "text": chunk,
                "metadata": {
                    "filename": filename,
                    "page": page_data["page"],
                    "chunk_index": ci,
                    "chunk_id": f"{filename}_p{page_data['page']}_c{ci}",
                },
            })
    return result
