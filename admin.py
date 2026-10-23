from datetime import date

import pandas as pd
import streamlit as st

from auth import hash_password
from config import ADMIN_USERNAME, ADMIN_PASSWORD
from database import get_all_students, username_exists, password_fingerprint_exists, insert_student
import hashlib


def show_error(msg):
    st.markdown(f"<div class='alert-error'>{msg}</div>", unsafe_allow_html=True)


def show_success(msg):
    st.markdown(f"<div class='alert-success'>{msg}</div>", unsafe_allow_html=True)


def admin_dashboard():
    st.sidebar.write("Welcome, Admin")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_type = None
        st.session_state.student = None
        st.rerun()

    st.markdown(
        """
        <div class='top-banner'>
            <h1>School Admin Dashboard</h1>
            <p>Manage real student records securely with unique usernames and passwords.</p>
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
            <div class='metric-card'>
                <div class='metric-label'>Total Students</div>
                <div class='metric-value'>{total_students}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("""
            <div class='metric-card'>
                <div class='metric-label'>Attendance</div>
                <div class='metric-value'>96%</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class='metric-card'>
                <div class='metric-label'>Fee Collection</div>
                <div class='metric-value'>87%</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class='metric-card'>
                <div class='metric-label'>Classes</div>
                <div class='metric-value'>24</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Add Student</div>", unsafe_allow_html=True)

    with st.form("student_form"):
        c1, c2 = st.columns(2)

        with c1:
            name = st.text_input("Full Name", key="name")
            dob = st.date_input("Date of Birth", value=date.today(), key="dob")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender")
            class_name = st.text_input("Class", key="class_name")
            section = st.text_input("Section", key="section")
            roll_number = st.text_input("Roll Number", key="roll_number")

        with c2:
            email = st.text_input("Email", key="email")
            phone = st.text_input("Phone", key="phone")
            address = st.text_area("Address", key="address")
            parent_name = st.text_input("Parent / Guardian Name", key="parent_name")
            parent_phone = st.text_input("Parent / Guardian Phone", key="parent_phone")
            username = st.text_input("Student Username", key="username")
            password = st.text_input("Student Password", type="password", key="password")

        submitted = st.form_submit_button("Save Student")

    if submitted:
        required_fields = [
            name,
            str(dob),
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
            password,
        ]

        if any(str(field).strip() == "" for field in required_fields):
            show_error("Please fill all required fields.")
            return

        if len(password.strip()) < 6:
            show_error("Password must be at least 6 characters long.")
            return

        if username_exists(username):
            show_error("Username already exists. Choose another username.")
            return

        if password_fingerprint_exists(password):
            show_error("This password already belongs to another student. Use a unique password.")
            return

        salt_b64, password_hash_b64 = hash_password(password)

        student_data = {
            "name": name.strip(),
            "dob": str(dob),
            "gender": gender,
            "class_name": class_name.strip(),
            "section": section.strip(),
            "roll_number": roll_number.strip(),
            "email": email.strip(),
            "phone": phone.strip(),
            "address": address.strip(),
            "parent_name": parent_name.strip(),
            "parent_phone": parent_phone.strip(),
            "username": username.strip(),
            "password_hash": password_hash_b64,
            "salt": salt_b64,
            "password_fingerprint": hashlib.sha256(password.strip().encode("utf-8")).hexdigest(),
        }

        ok, msg = insert_student(student_data)
        if ok:
            show_success(msg)
        else:
            show_error(msg)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Registered Students</div>", unsafe_allow_html=True)

    if students:
        df = pd.DataFrame(students)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No students registered yet.")
