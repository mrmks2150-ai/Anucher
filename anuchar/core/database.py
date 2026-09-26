import sqlite3
import os
from datetime import datetime

DB_PATH = "data/anuchar.db"


def _conn():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = _conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            created_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            content TEXT,
            created_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            prompt TEXT,
            style TEXT,
            created_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            done INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER PRIMARY KEY,
            model TEXT DEFAULT 'llama-3.1-8b-instant',
            provider TEXT DEFAULT 'groq',
            voice_lang TEXT DEFAULT 'hi-IN',
            auto_speak INTEGER DEFAULT 0,
            web_search INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()


def create_session(sid, user_id, title="New Chat"):
    conn = _conn()
    conn.execute(
        "INSERT OR IGNORE INTO sessions (id, user_id, title, created_at) VALUES (?, ?, ?, ?)",
        (sid, user_id, title, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def list_sessions(user_id):
    conn = _conn()
    rows = conn.execute(
        "SELECT id, title, created_at FROM sessions WHERE user_id=? ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def update_session_title(sid, title):
    conn = _conn()
    conn.execute("UPDATE sessions SET title=? WHERE id=?", (title[:40], sid))
    conn.commit()
    conn.close()


def delete_session(sid):
    conn = _conn()
    conn.execute("DELETE FROM chats WHERE session_id=?", (sid,))
    conn.execute("DELETE FROM sessions WHERE id=?", (sid,))
    conn.commit()
    conn.close()


def save_message(sid, user_id, role, content):
    conn = _conn()
    conn.execute(
        "INSERT INTO chats (session_id, user_id, role, content, timestamp) VALUES (?, ?, ?, ?, ?)",
        (sid, user_id, role, content, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def load_messages(sid):
    conn = _conn()
    rows = conn.execute(
        "SELECT role, content FROM chats WHERE session_id=? ORDER BY id ASC",
        (sid,),
    ).fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]


def save_document(user_id, name, content):
    conn = _conn()
    conn.execute(
        "INSERT INTO documents (user_id, name, content, created_at) VALUES (?, ?, ?, ?)",
        (user_id, name, content, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def list_documents(user_id):
    conn = _conn()
    rows = conn.execute(
        "SELECT id, name, created_at FROM documents WHERE user_id=? ORDER BY id DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def get_document(doc_id):
    conn = _conn()
    row = conn.execute(
        "SELECT name, content FROM documents WHERE id=?", (doc_id,)
    ).fetchone()
    conn.close()
    return row


def delete_document(doc_id):
    conn = _conn()
    conn.execute("DELETE FROM documents WHERE id=?", (doc_id,))
    conn.commit()
    conn.close()


def save_image(user_id, prompt, style):
    conn = _conn()
    conn.execute(
        "INSERT INTO images (user_id, prompt, style, created_at) VALUES (?, ?, ?, ?)",
        (user_id, prompt, style, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def list_images(user_id):
    conn = _conn()
    rows = conn.execute(
        "SELECT id, prompt, style, created_at FROM images WHERE user_id=? ORDER BY id DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def add_task(user_id, title):
    conn = _conn()
    conn.execute(
        "INSERT INTO tasks (user_id, title, created_at) VALUES (?, ?, ?)",
        (user_id, title, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def list_tasks(user_id):
    conn = _conn()
    rows = conn.execute(
        "SELECT id, title, done FROM tasks WHERE user_id=? ORDER BY done ASC, id DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def toggle_task(task_id):
    conn = _conn()
    conn.execute("UPDATE tasks SET done = 1 - done WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = _conn()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


def get_settings(user_id):
    conn = _conn()
    row = conn.execute(
        "SELECT model, provider, voice_lang, auto_speak, web_search FROM settings WHERE user_id=?",
        (user_id,),
    ).fetchone()
    if not row:
        conn.execute("INSERT INTO settings (user_id) VALUES (?)", (user_id,))
        conn.commit()
        row = ("llama-3.1-8b-instant", "groq", "hi-IN", 0, 1)
    conn.close()
    return {
        "model": row[0],
        "provider": row[1],
        "voice_lang": row[2],
        "auto_speak": bool(row[3]),
        "web_search": bool(row[4]),
    }


def update_settings(user_id, **kwargs):
    conn = _conn()
    for k, v in kwargs.items():
        conn.execute(f"UPDATE settings SET {k}=? WHERE user_id=?", (v, user_id))
    conn.commit()
    conn.close()


def get_stats(user_id):
    conn = _conn()
    s = {}
    s["sessions"] = conn.execute(
        "SELECT COUNT(*) FROM sessions WHERE user_id=?", (user_id,)
    ).fetchone()[0]
    s["messages"] = conn.execute(
        "SELECT COUNT(*) FROM chats WHERE user_id=?", (user_id,)
    ).fetchone()[0]
    s["documents"] = conn.execute(
        "SELECT COUNT(*) FROM documents WHERE user_id=?", (user_id,)
    ).fetchone()[0]
    s["images"] = conn.execute(
        "SELECT COUNT(*) FROM images WHERE user_id=?", (user_id,)
    ).fetchone()[0]
    s["tasks"] = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE user_id=?", (user_id,)
    ).fetchone()[0]

    rows = conn.execute("""
        SELECT DATE(timestamp) as day, COUNT(*)
        FROM chats WHERE user_id=?
        GROUP BY day ORDER BY day DESC LIMIT 7
    """, (user_id,)).fetchall()
    conn.close()
    s["daily"] = list(reversed(rows))
    return s


init_db()
