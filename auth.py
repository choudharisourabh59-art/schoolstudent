import base64
import hashlib
import hmac
import os

from database import get_student_by_username


def hash_password(password: str):
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000,
    )
    return base64.b64encode(salt).decode("utf-8"), base64.b64encode(pwd_hash).decode("utf-8")


def verify_password(password: str, salt_b64: str, password_hash_b64: str) -> bool:
    salt = base64.b64decode(salt_b64.encode("utf-8"))
    expected_hash = base64.b64decode(password_hash_b64.encode("utf-8"))
    computed_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000,
    )
    return hmac.compare_digest(computed_hash, expected_hash)


def login_student(username: str, password: str):
    row = get_student_by_username(username)
    if row is None:
        return None
    if verify_password(password, row["salt"], row["password_hash"]):
        return dict(row)
    return None
