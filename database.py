import sqlite3
from typing import List, Dict, Optional

from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dob TEXT NOT NULL,
            gender TEXT NOT NULL,
            class_name TEXT NOT NULL,
            section TEXT NOT NULL,
            roll_number TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            parent_name TEXT NOT NULL,
            parent_phone TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            password_fingerprint TEXT NOT NULL UNIQUE,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def get_all_students() -> List[Dict]:
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, name, dob, gender, class_name, section, roll_number,
               email, phone, address, parent_name, parent_phone, username
        FROM students ORDER BY name ASC
        """
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_student_by_username(username: str) -> Optional[Dict]:
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM students WHERE LOWER(username) = LOWER(?)",
        (username.strip(),),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)


def username_exists(username: str) -> bool:
    conn = get_connection()
    row = conn.execute(
        "SELECT 1 FROM students WHERE LOWER(username) = LOWER(?)",
        (username.strip(),),
    ).fetchone()
    conn.close()
    return row is not None


def password_fingerprint_exists(password: str) -> bool:
    import hashlib
    fingerprint = hashlib.sha256(password.strip().encode("utf-8")).hexdigest()
    conn = get_connection()
    row = conn.execute(
        "SELECT 1 FROM students WHERE password_fingerprint = ?",
        (fingerprint,),
    ).fetchone()
    conn.close()
    return row is not None


def insert_student(student_data: Dict) -> tuple[bool, str]:
    try:
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO students (
                name, dob, gender, class_name, section, roll_number,
                email, phone, address, parent_name, parent_phone,
                username, password_hash, salt, password_fingerprint
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_data["name"],
                student_data["dob"],
                student_data["gender"],
                student_data["class_name"],
                student_data["section"],
                student_data["roll_number"],
                student_data["email"],
                student_data["phone"],
                student_data["address"],
                student_data["parent_name"],
                student_data["parent_phone"],
                student_data["username"],
                student_data["password_hash"],
                student_data["salt"],
                student_data["password_fingerprint"],
            ),
        )
        conn.commit()
        conn.close()
        return True, "Student added successfully."
    except sqlite3.IntegrityError:
        return False, "Username or password duplicate detected. Please use unique values."
    except Exception as e:
        return False, f"Database error: {str(e)}"
