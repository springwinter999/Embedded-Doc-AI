from fastapi import APIRouter, HTTPException
from db.sqlite import get_db

router = APIRouter(tags=["conversations"])


@router.get("/conversations")
def list_conversations():
    db = get_db()
    rows = db.execute(
        """
        SELECT c.*, COUNT(m.id) as message_count
        FROM conversations c
        LEFT JOIN messages m ON c.id = m.conversation_id
        GROUP BY c.id
        ORDER BY c.updated_at DESC
        """
    ).fetchall()
    return {
        "conversations": [
            {
                "id": row["id"],
                "title": row["title"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "message_count": row["message_count"],
            }
            for row in rows
        ]
    }


@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str):
    db = get_db()
    row = db.execute(
        "SELECT id FROM conversations WHERE id = ?", (conversation_id,)
    ).fetchone()
    if not row:
        raise HTTPException(404, "对话不存在")
    db.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    db.commit()
    return {"status": "deleted", "conversation_id": conversation_id}
