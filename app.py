import streamlit as st

from auth import login_student
from admin import admin_dashboard, show_error
from student import student_dashboard
from config import ADMIN_USERNAME, ADMIN_PASSWORD
from database import init_db
from styles import CSS


st.set_page_config(page_title="School ERP", page_icon="🎓", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

init_db()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "student" not in st.session_state:
    st.session_state.student = None


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
            show_error("Invalid username or password.")


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


def logout():
    st.session_state.authenticated = False
    st.session_state.user_type = None
    st.session_state.student = None
    st.rerun()


if not st.session_state.authenticated:
    st.markdown(
        """
        <div class='top-banner'>
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
