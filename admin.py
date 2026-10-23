import pandas as pd
import streamlit as st

from dashboard import dashboard_home
from students import students_page
from attendance import attendance_page
from fees import fees_page
from grades import grades_page
from reports import reports_page
from utils import show_error

from config import ADMIN_USERNAME, ADMIN_PASSWORD
from auth import login_student


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


def admin_dashboard():
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Students", "Attendance", "Fees", "Grades", "Reports"],
        index=0
    )

    if page == "Dashboard":
        dashboard_home()
    elif page == "Students":
        students_page()
    elif page == "Attendance":
        attendance_page()
    elif page == "Fees":
        fees_page()
    elif page == "Grades":
        grades_page()
    elif page == "Reports":
        reports_page()
