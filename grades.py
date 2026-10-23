import pandas as pd
import streamlit as st

from database import get_all_students, insert_grade, get_student_grades


def grades_page():
    st.markdown("<div class='section-title'>Gradebook</div>", unsafe_allow_html=True)

    students = get_all_students()
    if not students:
        st.info("No students found. Add students first.")
        return

    student_names = [s["name"] for s in students]
    selected_name = st.selectbox("Select Student", student_names)

    selected_student = next(s for s in students if s["name"] == selected_name)
    student_id = selected_student["id"]

    with st.form("grade_form"):
        subject = st.text_input("Subject")
        exam_name = st.text_input("Exam Name")
        marks = st.number_input("Marks", min_value=0.0, max_value=100.0)
        max_marks = st.number_input("Maximum Marks", min_value=1.0, max_value=200.0)
        grade = st.text_input("Grade")
        exam_date = st.date_input("Exam Date")
        submitted = st.form_submit_button("Save Grade")

    if submitted:
        insert_grade(student_id, subject, exam_name, marks, max_marks, grade, str(exam_date))
        st.success("Grade entry saved successfully.")

    records = get_student_grades(student_id)
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)
    else:
        st.info("No grades recorded yet.")
