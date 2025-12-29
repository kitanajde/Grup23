# auth.py
import time
from typing import Tuple, Optional

from utils import generate_salt, hash_password, verify_password
from config import LOCKOUT_THRESHOLD, LOCKOUT_TIME
import db
import identity_disc


def is_locked(username: str) -> bool:
    locked_at = db.get_lockout(username)
    if locked_at is None:
        return False
    if time.time() - locked_at < LOCKOUT_TIME:
        return True
    db.clear_lockout(username)
    return False


def register_failed_attempt(username: str) -> None:
    current = db.get_failed_attempts(username)
    current += 1
    if current >= LOCKOUT_THRESHOLD:
        db.set_lockout(username, time.time())
        db.set_failed_attempts(username, 0)
    else:
        db.set_failed_attempts(username, current)


def reset_failed_attempts(username: str) -> None:
    db.set_failed_attempts(username, 0)


def register_user(username: str, password: str, role: str) -> bool:
    if db.get_user(username) is not None:
        return False

    salt_bytes = generate_salt()
    hashed, salt = hash_password(password, salt_bytes)

    created = db.create_user(username, hashed, salt, role)
    if created:
        identity_disc.on_register(username, role)
    return created


def login_user(username: str, password: str) -> Tuple[Optional[dict], str]:
    if is_locked(username):
        return None, "Account is temporarily locked."

    user = db.get_user(username)
    if not user:
        register_failed_attempt(username)
        return None, "Invalid user or password."

    if not verify_password(user["password"], password, user["salt"]):
        register_failed_attempt(username)
        return None, "Invalid user or password."

    reset_failed_attempts(username)
    identity_disc.on_login(username, user["role"])
    return user, "Login successful."
