import pandas as pd
import streamlit as st

from database import get_all_students


def dashboard_home():
    students = get_all_students()
    total_students = len(students)

    st.markdown(
        """
        <div class='top-banner'>
            <h1>School Admin Dashboard</h1>
            <p>Student operations, attendance, fee visibility, and academic monitoring in one place.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Total Students</div>
                <div class='metric-value'>{total_students}</div>
            </div>
        """, unsafe_allow_html=True)

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

    attendance_df = pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Attendance": [90, 92, 94, 93, 95, 96]
        }
    )

    fee_df = pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Collection": [70, 75, 80, 83, 88, 90]
        }
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Attendance Trend")
        st.line_chart(attendance_df.set_index("Month"), use_container_width=True)

    with c2:
        st.subheader("Fee Collection")
        st.line_chart(fee_df.set_index("Month"), use_container_width=True)
