# utils.py
import os
import hashlib
import base64


def generate_salt(length=16):
    return os.urandom(length)


def hash_password(password, salt: bytes):
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        200000
    )
    return base64.b64encode(dk).decode(), base64.b64encode(salt).decode()


def verify_password(stored_password: str, input_password: str, stored_salt: str) -> bool:
    salt = base64.b64decode(stored_salt)
    hashed, _ = hash_password(input_password, salt)
    return hashed == stored_password
