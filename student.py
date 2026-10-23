import pandas as pd
import streamlit as st

from database import get_student_attendance, get_fee_records, get_student_grades


def student_dashboard(student):
    st.sidebar.write(f"Welcome, {student['name']}")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_type = None
        st.session_state.student = None
        st.rerun()

    st.markdown(
        """
        <div class='top-banner'>
            <h1>Student Portal</h1>
            <p>Your academic, attendance, and fee information in a secure portal.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Name</div>
                <div class='metric-value' style='font-size:1.3rem;'>{student['name']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Class</div>
                <div class='metric-value' style='font-size:1.3rem;'>{student['class_name']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Section</div>
                <div class='metric-value' style='font-size:1.3rem;'>{student['section']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Roll No</div>
                <div class='metric-value' style='font-size:1.3rem;'>{student['roll_number']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    profile = {
        "Full Name": student["name"],
        "Date of Birth": student["dob"],
        "Gender": student["gender"],
        "Class": student["class_name"],
        "Section": student["section"],
        "Roll Number": student["roll_number"],
        "Email": student["email"],
        "Phone": student["phone"],
        "Address": student["address"],
        "Parent / Guardian": student["parent_name"],
        "Parent Phone": student["parent_phone"],
        "Username": student["username"],
    }

    st.subheader("Profile")
    st.dataframe(pd.DataFrame(list(profile.items()), columns=["Field", "Value"]), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    attendance = get_student_attendance(student["id"])
    if attendance:
        st.subheader("Attendance")
        st.dataframe(pd.DataFrame(attendance), use_container_width=True, hide_index=True)

    fee_records = get_fee_records(student["id"])
    if fee_records:
        st.subheader("Fee Details")
        st.dataframe(pd.DataFrame(fee_records), use_container_width=True, hide_index=True)

    grades = get_student_grades(student["id"])
    if grades:
        st.subheader("Grades")
        st.dataframe(pd.DataFrame(grades), use_container_width=True, hide_index=True)
