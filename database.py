import sqlite3
from typing import List, Dict, Optional

from config import DB_PATH


def get_connection() -> sqlite3.Connection:
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

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL,
            remarks TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS fee_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            total_fee REAL NOT NULL,
            paid_amount REAL NOT NULL DEFAULT 0,
            due_amount REAL NOT NULL,
            status TEXT NOT NULL,
            payment_date TEXT,
            remarks TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            exam_name TEXT NOT NULL,
            marks REAL NOT NULL,
            max_marks REAL NOT NULL,
            grade TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
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


def get_student_by_username(username: str) -> dict | None:
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
    fp = hashlib.sha256(password.strip().encode("utf-8")).hexdigest()
    conn = get_connection()
    row = conn.execute(
        "SELECT 1 FROM students WHERE password_fingerprint = ?",
        (fp,),
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
        return False, "Duplicate username or password found. Use unique values."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def insert_attendance(student_id: int, attendance_date: str, status: str, remarks: str = ""):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO attendance (student_id, attendance_date, status, remarks)
        VALUES (?, ?, ?, ?)
        """,
        (student_id, attendance_date, status, remarks),
    )
    conn.commit()
    conn.close()


def get_student_attendance(student_id: int):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT attendance_date, status, remarks
        FROM attendance
        WHERE student_id = ?
        ORDER BY attendance_date DESC
        """,
        (student_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def insert_fee_record(student_id: int, total_fee: float, paid_amount: float, due_amount: float, status: str, payment_date: str, remarks: str = ""):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO fee_records (student_id, total_fee, paid_amount, due_amount, status, payment_date, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (student_id, total_fee, paid_amount, due_amount, status, payment_date, remarks),
    )
    conn.commit()
    conn.close()


def get_fee_records(student_id: int):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT total_fee, paid_amount, due_amount, status, payment_date, remarks
        FROM fee_records
        WHERE student_id = ?
        ORDER BY payment_date DESC
        """,
        (student_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def insert_grade(student_id: int, subject: str, exam_name: str, marks: float, max_marks: float, grade: str, exam_date: str):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO grades (student_id, subject, exam_name, marks, max_marks, grade, exam_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (student_id, subject, exam_name, marks, max_marks, grade, exam_date),
    )
    conn.commit()
    conn.close()


def get_student_grades(student_id: int):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT subject, exam_name, marks, max_marks, grade, exam_date
        FROM grades
        WHERE student_id = ?
        ORDER BY exam_date DESC
        """,
        (student_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
