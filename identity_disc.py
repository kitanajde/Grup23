# identity_disc.py
import time
from typing import Optional, Dict

from db import get_connection


def _ensure_disc_row(username: str, role: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username FROM identity_disc WHERE username = ?", (username,))
    row = cur.fetchone()
    if not row:
        # Admin biraz daha yüksek security_level ile başlasın
        base_level = 3 if role == "admin" else 1
        cur.execute(
            "INSERT INTO identity_disc (username, role, security_level, "
            "commands_executed, threat_score, login_count, last_access) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (username, role, base_level, 0, 0, 0, None),
        )
        conn.commit()
    conn.close()


def on_register(username: str, role: str):
    _ensure_disc_row(username, role)


def on_login(username: str, role: str):
    conn = get_connection()
    cur = conn.cursor()
    _ensure_disc_row(username, role)
    cur.execute(
        "UPDATE identity_disc "
        "SET login_count = login_count + 1, last_access = ? "
        "WHERE username = ?",
        (time.time(), username),
    )
    conn.commit()
    conn.close()


def record_command(username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE identity_disc "
        "SET commands_executed = commands_executed + 1 "
        "WHERE username = ?",
        (username,),
    )
    conn.commit()
    conn.close()


def add_threat(username: str, delta: int):
    if delta <= 0:
        return
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE identity_disc "
        "SET threat_score = threat_score + ? "
        "WHERE username = ?",
        (delta, username),
    )
    conn.commit()
    conn.close()


def get_disc(username: str) -> Optional[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT username, role, security_level, commands_executed, "
        "threat_score, login_count, last_access "
        "FROM identity_disc WHERE username = ?",
        (username,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None

    last_access_str = "never"
    if row["last_access"] is not None:
        last_access_str = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(row["last_access"])
        )

    return {
        "username": row["username"],
        "role": row["role"],
        "security_level": row["security_level"],
        "commands_executed": row["commands_executed"],
        "threat_score": row["threat_score"],
        "login_count": row["login_count"],
        "last_access": last_access_str,
    }
