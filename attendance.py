import pandas as pd
import streamlit as st

from database import get_all_students, insert_attendance, get_student_attendance


def attendance_page():
    st.markdown("<div class='section-title'>Attendance Management</div>", unsafe_allow_html=True)

    students = get_all_students()
    if not students:
        st.info("No students found. Add students first.")
        return

    student_names = [s["name"] for s in students]
    selected_name = st.selectbox("Select Student", student_names)

    selected_student = next(s for s in students if s["name"] == selected_name)
    student_id = selected_student["id"]

    with st.form("attendance_form"):
        attendance_date = st.date_input("Attendance Date")
        status = st.selectbox("Status", ["Present", "Absent", "Late", "Excused"])
        remarks = st.text_area("Remarks")
        submitted = st.form_submit_button("Save Attendance")

    if submitted:
        insert_attendance(student_id, str(attendance_date), status, remarks)
        st.success("Attendance saved successfully.")

    records = get_student_attendance(student_id)
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)
    else:
        st.info("No attendance record yet.")
