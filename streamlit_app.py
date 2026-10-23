import os
import sqlite3
import base64
import hashlib
import hmac
from datetime import date

import pandas as pd
import streamlit as st

DB_PATH = "school_data.db"

# ---- Default admin credentials ----
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@123")


# -----------------------------
# DB helpers
# -----------------------------
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


def username_exists(username):
    conn = get_connection()
    row = conn.execute(
        "SELECT 1 FROM students WHERE LOWER(username) = LOWER(?)",
        (username.strip(),),
    ).fetchone()
    conn.close()
    return row is not None


def password_fingerprint_exists(password):
    fingerprint = hashlib.sha256(password.strip().encode("utf-8")).hexdigest()
    conn = get_connection()
    row = conn.execute(
        "SELECT 1 FROM students WHERE password_fingerprint = ?",
        (fingerprint,),
    ).fetchone()
    conn.close()
    return row is not None


def hash_password(password):
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )
    return base64.b64encode(salt).decode("utf-8"), base64.b64encode(pwd_hash).decode("utf-8")


def verify_password(password, salt_b64, password_hash_b64):
    salt = base64.b64decode(salt_b64.encode("utf-8"))
    expected_hash = base64.b64decode(password_hash_b64.encode("utf-8"))
    computed_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )
    return hmac.compare_digest(computed_hash, expected_hash)


def add_student(student_data):
    required = [
        "name",
        "dob",
        "gender",
        "class_name",
        "section",
        "roll_number",
        "email",
        "phone",
        "address",
        "parent_name",
        "parent_phone",
        "username",
        "password"
    ]

    for field in required:
        if field not in student_data or not str(student_data[field]).strip():
            return False, f"Field '{field}' is required."

    # sanitize inputs
    name = student_data["name"].strip()
    dob = str(student_data["dob"]).strip()
    gender = student_data["gender"].strip()
    class_name = student_data["class_name"].strip()
    section = student_data["section"].strip()
    roll_number = student_data["roll_number"].strip()
    email = student_data["email"].strip()
    phone = student_data["phone"].strip()
    address = student_data["address"].strip()
    parent_name = student_data["parent_name"].strip()
    parent_phone = student_data["parent_phone"].strip()
    username = student_data["username"].strip()
    password = student_data["password"].strip()

    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    if username_exists(username):
        return False, "Username already exists. Use a different username."

    if password_fingerprint_exists(password):
        return False, "This password already exists for another student. Please choose a unique password."

    salt_b64, password_hash_b64 = hash_password(password)
    fingerprint = hashlib.sha256(password.encode("utf-8")).hexdigest()

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
                name,
                dob,
                gender,
                class_name,
                section,
                roll_number,
                email,
                phone,
                address,
                parent_name,
                parent_phone,
                username,
                password_hash_b64,
                salt_b64,
                fingerprint,
            ),
        )
        conn.commit()
        conn.close()
        return True, "Student added successfully."
    except sqlite3.IntegrityError:
        return False, "Duplicate entry detected. Please verify username and password."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def login_student(username, password):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM students WHERE LOWER(username) = LOWER(?)",
        (username.strip(),),
    ).fetchone()
    conn.close()

    if row is None:
        return None

    if verify_password(password, row["salt"], row["password_hash"]):
        return dict(row)

    return None


def get_all_students():
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


# -----------------------------
# UI styling
# -----------------------------
st.set_page_config(page_title="School ERP", page_icon="🎓", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #eef3ff;
        --bg-2: #f7f9ff;
        --panel: rgba(255,255,255,0.92);
        --sidebar: #09111d;
        --sidebar-2: #111c2d;
        --primary: #2f6ef8;
        --primary-2: #4f46e5;
        --primary-soft: #e8f0ff;
        --success: #21b070;
        --warning: #f59e0b;
        --danger: #ef4444;
        --text: #101827;
        --muted: #667085;
        --line: #e5e7eb;
        --shadow: 0 18px 40px rgba(31,41,55,0.10);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #edf2ff 0%, #f7f9ff 100%);
        font-family: 'Inter', sans-serif;
        color: var(--text);
    }

    .main {
        background: transparent;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
    }

    .panel {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 20px;
        box-shadow: var(--shadow);
        padding: 22px;
    }

    .top-banner {
        background: linear-gradient(90deg, #1f5ae9 0%, #4f46e5 100%);
        color: white;
        border-radius: 20px;
        padding: 24px 28px;
        box-shadow: 0 18px 32px rgba(79, 70, 229, 0.18);
    }

    .top-banner h1 {
        margin: 0;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.05em;
    }

    .top-banner p {
        margin: 8px 0 0 0;
        font-size: 0.96rem;
        opacity: 0.9;
    }

    .metric-card {
        background: rgba(255,255,255,0.95);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 20px 18px;
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.05);
        min-height: 142px;
    }

    .metric-label {
        font-size: 0.75rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
    }

    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        margin-top: 12px;
        letter-spacing: -0.05em;
        color: var(--text);
    }

    .btn-primary {
        background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%);
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.3rem !important;
        font-weight: 700 !important;
    }

    .btn-primary:hover {
        filter: brightness(1.05);
    }

    .stButton > button {
        background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.25rem;
        font-weight: 700;
        box-shadow: 0 12px 20px rgba(79,70,229,0.18);
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox select, .stDateInput input {
        border-radius: 12px;
        border: 1px solid #d1d5db;
        padding: 0.78rem 0.9rem;
        background: white;
    }

    .alert-success {
        color: #047857;
        background: rgba(16,185,129,0.08);
        border: 1px solid rgba(16,185,129,0.18);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        font-weight: 700;
    }

    .alert-error {
        color: #b91c1c;
        background: rgba(239,68,68,0.08);
        border: 1px solid rgba(239,68,68,0.18);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        font-weight: 700;
    }

    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #0a1020 0%, #111c2d 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1020 0%, #111c2d 100%);
    }

    [data-testid="stSidebarNav"] a {
        border-radius: 12px;
        margin: 6px 8px;
        padding: 10px 12px;
        color: white;
    }

    [data-testid="stSidebarNav"] a[data-selected="true"] {
        background: linear-gradient(90deg, #2563eb, #4f46e5);
        font-weight: 700;
    }

    .stat-badge {
        display: inline-block;
        background: linear-gradient(90deg, #e8f0ff, #eef2ff);
        color: #1d4ed8;
        border: 1px solid #dbeafe;
        border-radius: 999px;
        padding: 6px 12px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: var(--text);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

init_db()

# -----------------------------
# Session states
# -----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "student" not in st.session_state:
    st.session_state.student = None


def show_error(msg):
    st.markdown(f"<div class='alert-error'>{msg}</div>", unsafe_allow_html=True)


def show_success(msg):
    st.markdown(f"<div class='alert-success'>{msg}</div>", unsafe_allow_html=True)


def logout():
    st.session_state.authenticated = False
    st.session_state.user_type = None
    st.session_state.student = None
    st.rerun()


# -----------------------------
# Login pages
# -----------------------------
def admin_login_page():
    st.title("Admin Login")
    with st.form("admin_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.user_type = "admin"
            st.session_state.student = None
            st.rerun()
        else:
            show_error("Invalid admin username or password.")


def student_login_page():
    st.title("Student Login")
    with st.form("student_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if not username.strip() or not password.strip():
            show_error("Please enter a valid username and password.")
            return

        student = login_student(username, password)
        if student:
            st.session_state.authenticated = True
            st.session_state.user_type = "student"
            st.session_state.student = student
            st.rerun()
        else:
            show_error("Invalid username or password.")


# -----------------------------
# Admin dashboard
# -----------------------------
def admin_dashboard():
    st.sidebar.write("Welcome, Admin")
    st.sidebar.button("Logout", on_click=logout)

    st.markdown(
        """
        <div class="top-banner">
            <h1>School Admin Dashboard</h1>
            <p>Manage student records securely with unique usernames and protected passwords.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    students = get_all_students()
    total_students = len(students)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Students</div>
                <div class="metric-value">{total_students}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Attendance</div>
                <div class="metric-value">96%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Fee Collection</div>
                <div class="metric-value">87%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Classes</div>
                <div class="metric-value">24</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<div class='section-title'>Add Student</div>",
        unsafe_allow_html=True,
    )

    with st.form("add_student_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name")
            dob = st.date_input("Date of Birth", value=date.today())
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            class_name = st.text_input("Class")
            section = st.text_input("Section")
            roll_number = st.text_input("Roll Number")

        with col2:
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            address = st.text_area("Address")
            parent_name = st.text_input("Parent / Guardian Name")
            parent_phone = st.text_input("Parent / Guardian Phone")
            username = st.text_input("Student Username")
            password = st.text_input("Student Password", type="password")

        submitted = st.form_submit_button("Save Student")

    if submitted:
        data = {
            "name": name,
            "dob": str(dob),
            "gender": gender,
            "class_name": class_name,
            "section": section,
            "roll_number": roll_number,
            "email": email,
            "phone": phone,
            "address": address,
            "parent_name": parent_name,
            "parent_phone": parent_phone,
            "username": username,
            "password": password,
        }
        ok, msg = add_student(data)
        if ok:
            show_success(msg)
        else:
            show_error(msg)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-title'>Registered Students</div>",
        unsafe_allow_html=True,
    )

    if students:
        df = pd.DataFrame(students)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No students registered yet.")


# -----------------------------
# Student dashboard
# -----------------------------
def student_dashboard(student):
    st.sidebar.write(f"Welcome, {student['name']}")
    st.sidebar.button("Logout", on_click=logout)

    st.markdown(
        """
        <div class="top-banner">
            <h1>Student Profile</h1>
            <p>Secure personal record for academic and profile management.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Name</div>
                <div class="metric-value" style="font-size:1.3rem;">{student['name']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Class</div>
                <div class="metric-value" style="font-size:1.3rem;">{student['class_name']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Section</div>
                <div class="metric-value" style="font-size:1.3rem;">{student['section']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Roll Number</div>
                <div class="metric-value" style="font-size:1.3rem;">{student['roll_number']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    profile_data = {
        "Full Name": student["name"],
        "Date of Birth": student["dob"],
        "Gender": student["gender"],
        "Email": student["email"],
        "Phone": student["phone"],
        "Address": student["address"],
        "Parent / Guardian": student["parent_name"],
        "Parent Phone": student["parent_phone"],
        "Username": student["username"],
        "Class": student["class_name"],
        "Section": student["section"],
    }

    st.markdown(
        "<div class='section-title'>Student Information</div>",
        unsafe_allow_html=True,
    )
    st.dataframe(pd.DataFrame(list(profile_data.items()), columns=["Field", "Value"]), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<div class='section-title'>Academic Summary</div>",
        unsafe_allow_html=True,
    )
    academic = pd.DataFrame(
        [
            {"Subject": "Mathematics", "Marks": "92", "Grade": "A+"},
            {"Subject": "Science", "Marks": "89", "Grade": "A"},
            {"Subject": "English", "Marks": "94", "Grade": "A+"},
            {"Subject": "Computer", "Marks": "96", "Grade": "A+"},
        ]
    )
    st.dataframe(academic, use_container_width=True, hide_index=True)


# -----------------------------
# Landing page with login choice
# -----------------------------
if not st.session_state.authenticated:
    st.markdown(
        """
        <div class="top-banner">
            <h1>School Student Information System</h1>
            <p>Secure portal for student registration, login, and profile access.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    login_type = st.selectbox("Login As", ["Student", "Admin"], index=0)
    if login_type == "Student":
        student_login_page()
    else:
        admin_login_page()
else:
    if st.session_state.user_type == "admin":
        admin_dashboard()
    elif st.session_state.user_type == "student":
        student_dashboard(st.session_state.student)
    else:
        logout()
