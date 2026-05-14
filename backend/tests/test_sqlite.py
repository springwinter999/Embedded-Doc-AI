import pytest
from db.sqlite import get_db, init_db


@pytest.fixture
def db():
    init_db(":memory:")
    yield


def test_init_creates_tables(db):
    conn = get_db()
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = [row[0] for row in cursor.fetchall()]
    assert "conversations" in tables
    assert "messages" in tables


def test_insert_conversation(db):
    conn = get_db()
    conn.execute(
        "INSERT INTO conversations (id, title) VALUES (?, ?)",
        ("conv-1", "Test conversation"),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM conversations WHERE id = ?", ("conv-1",)).fetchone()
    assert row["title"] == "Test conversation"


def test_insert_message(db):
    conn = get_db()
    conn.execute(
        "INSERT INTO conversations (id, title) VALUES (?, ?)",
        ("conv-1", "Test"),
    )
    conn.commit()
    conn.execute(
        "INSERT INTO messages (id, conversation_id, role, content, sources) VALUES (?, ?, ?, ?, ?)",
        ("msg-1", "conv-1", "user", "Hello", "[]"),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM messages WHERE id = ?", ("msg-1",)).fetchone()
    assert row["role"] == "user"
    assert row["content"] == "Hello"
