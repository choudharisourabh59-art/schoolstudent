import pandas as pd
import streamlit as st

from database import get_all_students, insert_fee_record, get_fee_records


def fees_page():
    st.markdown("<div class='section-title'>Fee Management</div>", unsafe_allow_html=True)

    students = get_all_students()
    if not students:
        st.info("No students found. Add students first.")
        return

    student_names = [s["name"] for s in students]
    selected_name = st.selectbox("Select Student", student_names)

    selected_student = next(s for s in students if s["name"] == selected_name)
    student_id = selected_student["id"]

    with st.form("fee_form"):
        total_fee = st.number_input("Total Fee", min_value=0.0, step=100.0)
        paid_amount = st.number_input("Paid Amount", min_value=0.0, step=50.0)
        due_amount = st.number_input("Due Amount", min_value=0.0, step=50.0)
        status = st.selectbox("Payment Status", ["Paid", "Pending", "Overdue"])
        payment_date = st.date_input("Payment Date")
        remarks = st.text_area("Remarks")
        submitted = st.form_submit_button("Save Fee Record")

    if submitted:
        insert_fee_record(student_id, total_fee, paid_amount, due_amount, status, str(payment_date), remarks)
        st.success("Fee record saved successfully.")

    records = get_fee_records(student_id)
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)
    else:
        st.info("No fee records found.")
