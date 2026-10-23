from datetime import date
import hashlib
import pandas as pd
import streamlit as st

from auth import hash_password
from database import get_all_students, username_exists, password_fingerprint_exists, insert_student
from utils import show_error, show_success


def students_page():
    st.markdown(
        "<div class='section-title'>Student Management</div>",
        unsafe_allow_html=True,
    )

    with st.form("student_form"):
        c1, c2 = st.columns(2)

        with c1:
            name = st.text_input("Full Name")
            dob = st.date_input("Date of Birth", value=date.today())
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            class_name = st.text_input("Class")
            section = st.text_input("Section")
            roll_number = st.text_input("Roll Number")

        with c2:
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            address = st.text_area("Address")
            parent_name = st.text_input("Parent / Guardian Name")
            parent_phone = st.text_input("Parent / Guardian Phone")
            username = st.text_input("Student Username")
            password = st.text_input("Student Password", type="password")

        submitted = st.form_submit_button("Save Student")

    if submitted:
        required = [
            name, str(dob), gender, class_name, section, roll_number,
            email, phone, address, parent_name, parent_phone, username, password
        ]

        if any(str(item).strip() == "" for item in required):
            show_error("Please fill all fields.")
            return

        if len(password.strip()) < 6:
            show_error("Password must be at least 6 characters long.")
            return

        if username_exists(username):
            show_error("Username already exists. Please choose a different one.")
            return

        if password_fingerprint_exists(password):
            show_error("This password already belongs to another student.")
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
    students = get_all_students()
    if students:
        st.dataframe(pd.DataFrame(students), use_container_width=True, hide_index=True)
    else:
        st.info("No students registered yet.")
