# streamlit_app.py
import streamlit as st

st.set_page_config(page_title="School Student Information System", page_icon="🏫", layout="wide")

st.title("School Student Information System")

# Top KPI cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Students", "15,000")
with col2:
    st.metric("Attendance Rate", "94.6%")
with col3:
    st.metric("Fee Collection", "87.4%")
with col4:
    st.metric("Average Marks", "83.2%")

st.markdown("---")

# Summary
st.subheader("School Overview")
st.write("A modern school management system for students, teachers, parents, and administrators.")

# tables / data
students = [
    {"Name": "Aarav Sharma", "Class": "10-A", "Attendance": "96%", "Average": "88%", "Fee": "Paid"},
    {"Name": "Meera Patel", "Class": "9-B", "Attendance": "91%", "Average": "84%", "Fee": "Partial"},
    {"Name": "Vihaan Reddy", "Class": "8-C", "Attendance": "94%", "Average": "90%", "Fee": "Paid"},
    {"Name": "Saanvi Nair", "Class": "7-A", "Attendance": "93%", "Average": "86%", "Fee": "Paid"},
]

st.dataframe(students, use_container_width=True)

# alerts
st.subheader("Alerts")
st.warning("12 students need attendance follow-up")
st.warning("48 fee reminders are pending for parents")
st.warning("3 new grade submissions are waiting for approval")

# simple charts
import pandas as pd

df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "Attendance": [92, 93, 94, 95, 96],
    "Fee Collection": [70, 74, 85, 81, 88]
})

col1, col2 = st.columns(2)
with col1:
    st.line_chart(df.set_index("Month")["Attendance"], use_container_width=True)

with col2:
    st.line_chart(df.set_index("Month")["Fee Collection"], use_container_width=True)

st.markdown("---")

st.subheader("Admin Controls")
st.button("Add Student")
st.button("Generate Report")
