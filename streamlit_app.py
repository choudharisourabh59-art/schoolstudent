import os
import sqlite3
import hashlib
from datetime import datetime

import streamlit as st
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash


DB_PATH = "school_data.db"

# Admin credentials
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@123")

# -----------------------------
# Database setup
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
    fp = hashlib.sha256(password.strip().encode("utf-8")).hexdigest()
    conn = get_connection()
    row = conn.execute(
        "SELECT 1 FROM students WHERE password_fingerprint = ?",
        (fp,),
    ).fetchone()
    conn.close()
    return row is not None


def add_student(student_data):
    required_fields = [
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
        "password",
    ]

    for field in required_fields:
        if field not in student_data or not str(student_data[field]).strip():
            return False, f"Field '{field}' is required."

    name = student_data["name"].strip()
    dob = student_data["dob"].strip()
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
        return False, "This username already exists. Please choose another one."

    if password_fingerprint_exists(password):
        return False, "This password is already in use. Please choose another password."

    password_hash = generate_password_hash(password, method="pbkdf2:sha256")
    password_fingerprint = hashlib.sha256(password.encode("utf-8")).hexdigest()

    try:
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO students (
                name, dob, gender, class_name, section, roll_number,
                email, phone, address, parent_name, parent_phone,
                username, password_hash, password_fingerprint
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                password_hash,
                password_fingerprint,
            ),
        )
        conn.commit()
        conn.close()
        return True, "Student added successfully."
    except sqlite3.IntegrityError:
        return False, "Duplicate data entered. Please check username and password again."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def login_student(username, password):
    conn = get_connection()
    student = conn.execute(
        """
        SELECT * FROM students
        WHERE LOWER(username) = LOWER(?)
        """,
        (username.strip(),),
    ).fetchone()
    conn.close()

    if student is None:
        return None

    if check_password_hash(student["password_hash"], password):
        return dict(student)

    return None


def get_all_students():
    conn = get_connection()
    students = conn.execute(
        """
        SELECT id, name, dob, gender, class_name, section, roll_number,
               email, phone, address, parent_name, parent_phone, username
        FROM students
        ORDER BY name ASC
        """
    ).fetchall()
    conn.close()
    return [dict(row) for row in students]


def get_student_by_username(username):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM students WHERE LOWER(username) = LOWER(?)",
        (username.strip(),),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)


# -----------------------------
# Styles
# -----------------------------
st.set_page_config(page_title="School Portal", page_icon="🎓", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #eef2ff 0%, #f8fafe 100%);
        color: #0f172a;
    }

    .main {
        background: transparent;
    }

    .card {
        background: rgba(255,255,255,0.96);
        border: 1px solid #e5e7eb;
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    }

    .header {
        background: linear-gradient(135deg, #1d4ed8 0%, #4f46e5 100%);
        color: white;
        border-radius: 22px;
        padding: 26px 28px;
        margin-bottom: 18px;
        box-shadow: 0 18px 30px rgba(79, 70, 229, 0.25);
    }

    .header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 800;
    }

    .header p {
        margin-top: 8px;
        margin-bottom: 0;
        opacity: 0.9;
    }

    .metric {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    }

    .metric-title {
        font-size: 0.78rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 8px;
    }

    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
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

    .stButton > button {
        background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.2rem;
        font-weight: 700;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox select, .stDateInput input {
        border-radius: 12px;
        border: 1px solid #d1d5db;
        padding: 0.7rem 0.9rem;
    }

    .success {
        color: #047857;
        font-weight: 700;
    }

    .error {
        color: #b91c1c;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

init_db()

# -----------------------------
# Session state defaults
# -----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "student" not in st.session_state:
    st.session_state.student = None


# -----------------------------
# Helpers for UI
# -----------------------------
def show_error(message):
    st.markdown(f"<div class='error'>{message}</div>", unsafe_allow_html=True)


def show_success(message):
    st.markdown(f"<div class='success'>{message}</div>", unsafe_allow_html=True)


# -----------------------------
# Admin login
# -----------------------------
def admin_login():
    st.title("Admin Login")
    with st.form("admin_form"):
        username = st.text_input("Admin Username", value=ADMIN_USERNAME)
        password = st.text_input("Admin Password", type="password")
        submitted = st.form_submit_button("Login as Admin")

    if submitted:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.user_type = "admin"
            st.session_state.student = None
            st.rerun()
        else:
            show_error("Invalid admin username or password.")


# -----------------------------
# Student login
# -----------------------------
def student_login():
    st.title("Student Login")
    with st.form("student_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login as Student")

    if submitted:
        if not username.strip() or not password.strip():
            show_error("Please enter username and password.")
        else:
            student = login_student(username, password)
            if student:
                st.session_state.authenticated = True
                st.session_state.user_type = "student"
                st.session_state.student = student
                st.rerun()
            else:
                show_error("Invalid username or password.")


# -----------------------------
# Logout
# -----------------------------
def logout():
    st.session_state.authenticated = False
    st.session_state.user_type = None
    st.session_state.student = None
    st.rerun()


# -----------------------------
# Admin dashboard
# -----------------------------
def admin_dashboard():
    st.sidebar.write("Welcome, Admin")
    st.sidebar.button("Logout", on_click=logout)

    st.markdown(
        """
        <div class="header">
            <h1>School Admin Dashboard</h1>
            <p>Manage students securely, add records, and protect login credentials.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    total_students = len(get_all_students())
    with col1:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-title">Total Students</div>
                <div class="metric-value">{total_students}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="metric">
                <div class="metric-title">Attendance</div>
                <div class="metric-value">96%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="metric">
                <div class="metric-title">Fee Collection</div>
                <div class="metric-value">87%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="metric">
                <div class="metric-title">Active Classes</div>
                <div class="metric-value">24</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Add New Student")
    with st.form("student_registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            dob = st.date_input("Date of Birth")
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
        student_data = {
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

        ok, msg = add_student(student_data)
        if ok:
            show_success(msg)
        else:
            show_error(msg)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Registered Students")
    students_df = pd.DataFrame(get_all_students())
    if not students_df.empty:
        st.dataframe(students_df, use_container_width=True)
    else:
        st.info("No students added yet.")


# -----------------------------
# Student dashboard
# -----------------------------
def student_dashboard(student):
    st.sidebar.write(f"Welcome, {student['name']}")
    st.sidebar.button("Logout", on_click=logout)

    st.markdown(
        """
        <div class="header">
            <h1>Student Profile</h1>
            <p>Personal details, class information, and student account information.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-title">Name</div>
                <div class="metric-value" style="font-size:1.4rem;">{student['name']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-title">Class</div>
                <div class="metric-value" style="font-size:1.4rem;">{student['class_name']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-title">Section</div>
                <div class="metric-value" style="font-size:1.4rem;">{student['section']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-title">Roll No</div>
                <div class="metric-value" style="font-size:1.4rem;">{student['roll_number']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    profile = {
        "Full Name": student["name"],
        "Date of Birth": student["dob"],
        "Gender": student["gender"],
        "Email": student["email"],
        "Phone": student["phone"],
        "Address": student["address"],
        "Parent / Guardian": student["parent_name"],
        "Parent Phone": student["parent_phone"],
        "Username": student["username"],
    }

    st.subheader("Personal Information")
    df = pd.DataFrame(list(profile.items()), columns=["Field", "Value"])
    st.dataframe(df, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Academic Summary")
    academic = pd.DataFrame(
        [
            {"Subject": "Mathematics", "Marks": "92", "Grade": "A+"},
            {"Subject": "Science", "Marks": "89", "Grade": "A"},
            {"Subject": "English", "Marks": "94", "Grade": "A+"},
            {"Subject": "Computer", "Marks": "96", "Grade": "A+"},
        ]
    )
    st.dataframe(academic, use_container_width=True)


# -----------------------------
# Main app
# -----------------------------
if not st.session_state.authenticated:
    st.markdown(
        """
        <div class="header">
            <h1>School Student Information System</h1>
            <p>Secure student management portal for real student accounts, login, and profile data.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    login_choice = st.selectbox("Login As", ["Student", "Admin"])
    if login_choice == "Student":
        student_login()
    else:
        admin_login()
else:
    if st.session_state.user_type == "admin":
        admin_dashboard()
    elif st.session_state.user_type == "student":
        student_dashboard(st.session_state.student)
    else:
        logout()
