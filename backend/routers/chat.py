import json
import uuid
from fastapi import APIRouter, HTTPException
from models.chat import ChatRequest
from services import vector_store, llm
from db.sqlite import get_db

router = APIRouter(tags=["chat"])


@router.post("/chat")
def chat(req: ChatRequest):
    """Main RAG Q&A endpoint."""
    db = get_db()

    context = vector_store.search(req.question)

    messages = llm.build_prompt(req.question, context)
    answer = llm.ask(messages)

    conversation_id = req.conversation_id
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        title = req.question[:40] + ("..." if len(req.question) > 40 else "")
        db.execute(
            "INSERT INTO conversations (id, title) VALUES (?, ?)",
            (conversation_id, title),
        )
        db.commit()
    else:
        row = db.execute(
            "SELECT id FROM conversations WHERE id = ?", (conversation_id,)
        ).fetchone()
        if not row:
            raise HTTPException(404, "对话不存在")
        db.execute(
            "UPDATE conversations SET updated_at = datetime('now', 'localtime') WHERE id = ?",
            (conversation_id,),
        )
        db.commit()

    sources = [
        {
            "page": c["metadata"].get("page", 0),
            "filename": c["metadata"].get("filename", ""),
            "snippet": c["text"][:200],
            "chunk_id": c["id"],
        }
        for c in context
    ]

    user_msg_id = str(uuid.uuid4())
    ai_msg_id = str(uuid.uuid4())

    db.execute(
        "INSERT INTO messages (id, conversation_id, role, content, sources) VALUES (?, ?, ?, ?, ?)",
        (user_msg_id, conversation_id, "user", req.question, "[]"),
    )
    db.execute(
        "INSERT INTO messages (id, conversation_id, role, content, sources) VALUES (?, ?, ?, ?, ?)",
        (ai_msg_id, conversation_id, "assistant", answer, json.dumps(sources, ensure_ascii=False)),
    )
    db.commit()

    return {
        "answer": answer,
        "conversation_id": conversation_id,
        "sources": sources,
        "message_id": ai_msg_id,
    }


@router.get("/chat/{conversation_id}")
def get_chat_history(conversation_id: str):
    """Get all messages for a conversation."""
    db = get_db()

    conv = db.execute(
        "SELECT * FROM conversations WHERE id = ?", (conversation_id,)
    ).fetchone()
    if not conv:
        raise HTTPException(404, "对话不存在")

    rows = db.execute(
        "SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
        (conversation_id,),
    ).fetchall()

    messages = []
    for row in rows:
        sources = []
        try:
            sources = json.loads(row["sources"] or "[]")
        except json.JSONDecodeError:
            pass
        messages.append({
            "id": row["id"],
            "role": row["role"],
            "content": row["content"],
            "sources": sources,
            "created_at": row["created_at"],
        })

    return {
        "conversation_id": conversation_id,
        "title": conv["title"],
        "messages": messages,
    }
