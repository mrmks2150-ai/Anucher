import sqlite3
import hashlib
import os
import secrets
from datetime import datetime

DB_PATH = "data/anuchar.db"


def _conn():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def _hash(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"{salt}${h.hex()}"


def _verify(password, stored):
    try:
        salt, _ = stored.split("$", 1)
        return _hash(password, salt) == stored
    except Exception:
        return False


def init_auth():
    conn = _conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def signup(username, password):
    if not username or not password:
        return False, "Username aur password zaroori hai."
    if len(username) < 3:
        return False, "Username kam se kam 3 characters ka ho."
    if len(password) < 4:
        return False, "Password kam se kam 4 characters ka ho."

    conn = _conn()
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (username.strip().lower(), _hash(password), datetime.now().isoformat()),
        )
        conn.commit()
        return True, "Account ban gaya! Ab login karo."
    except sqlite3.IntegrityError:
        return False, "Ye username already exist karta hai."
    finally:
        conn.close()


def login(username, password):
    conn = _conn()
    row = conn.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username.strip().lower(),),
    ).fetchone()
    conn.close()

    if not row:
        return False, "User nahi mila."
    user_id, stored = row
    if _verify(password, stored):
        return True, user_id
    return False, "Galat password."


init_auth()
