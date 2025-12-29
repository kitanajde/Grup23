# db.py
import sqlite3
import time
from typing import Optional, List, Dict

from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Kullanıcılar
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Failed attempts
    cur.execute("""
        CREATE TABLE IF NOT EXISTS failed_attempts (
            username TEXT PRIMARY KEY,
            count INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Lockout
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lockout (
            username TEXT PRIMARY KEY,
            locked_at REAL NOT NULL
        )
    """)

    # Komut logları (audit trail)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS command_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            cmd TEXT NOT NULL,
            created_at REAL NOT NULL
        )
    """)

    # Identity Disc tablosu
    cur.execute("""
        CREATE TABLE IF NOT EXISTS identity_disc (
            username TEXT PRIMARY KEY,
            role TEXT NOT NULL,
            security_level INTEGER NOT NULL,
            commands_executed INTEGER NOT NULL,
            threat_score INTEGER NOT NULL,
            login_count INTEGER NOT NULL,
            last_access REAL
        )
    """)

    conn.commit()
    conn.close()


# ---- User işlemleri ----

def get_user(username: str) -> Optional[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, password, salt, role FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "username": row["username"],
            "password": row["password"],
            "salt": row["salt"],
            "role": row["role"],
        }
    return None


def create_user(username: str, password: str, salt: str, role: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password, salt, role) VALUES (?, ?, ?, ?)",
            (username, password, salt, role),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def list_users() -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, role FROM users ORDER BY username")
    rows = cur.fetchall()
    conn.close()
    return [{"username": r["username"], "role": r["role"]} for r in rows]


# ---- Failed attempts / Lockout ----

def get_failed_attempts(username: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count FROM failed_attempts WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return int(row["count"])
    return 0


def set_failed_attempts(username: str, count: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO failed_attempts (username, count) VALUES (?, ?) "
        "ON CONFLICT(username) DO UPDATE SET count=excluded.count",
        (username, count),
    )
    conn.commit()
    conn.close()


def get_lockout(username: str) -> Optional[float]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT locked_at FROM lockout WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return float(row["locked_at"])
    return None


def set_lockout(username: str, locked_at: float) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO lockout (username, locked_at) VALUES (?, ?) "
        "ON CONFLICT(username) DO UPDATE SET locked_at=excluded.locked_at",
        (username, locked_at),
    )
    conn.commit()
    conn.close()


def clear_lockout(username: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM lockout WHERE username = ?", (username,))
    conn.commit()
    conn.close()


# ---- Komut logları ----

def log_command(username: str, cmd: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO command_log (username, cmd, created_at) VALUES (?, ?, ?)",
        (username, cmd, time.time()),
    )
    conn.commit()
    conn.close()


def get_recent_commands(limit: int = 20) -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT username, cmd, created_at FROM command_log ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "username": r["username"],
            "cmd": r["cmd"],
            "created_at": r["created_at"],
        }
        for r in rows
    ]
