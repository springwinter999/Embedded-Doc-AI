from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None


class SourceReference(BaseModel):
    page: int
    filename: str
    snippet: str
    chunk_id: str


class ChatResponse(BaseModel):
    answer: str
    conversation_id: str
    sources: list[dict]
    message_id: str
