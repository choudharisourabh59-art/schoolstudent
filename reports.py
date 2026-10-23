import pandas as pd
import streamlit as st


def reports_page():
    st.markdown("<div class='section-title'>Reports & Analytics</div>", unsafe_allow_html=True)

    attendance_df = pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Attendance": [92, 93, 94, 95, 96, 97],
            "Fee Collection": [70, 74, 80, 82, 88, 90],
        }
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Attendance Trend")
        st.line_chart(attendance_df.set_index("Month")["Attendance"], use_container_width=True)
    with c2:
        st.subheader("Fee Trend")
        st.line_chart(attendance_df.set_index("Month")["Fee Collection"], use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("School Summary")
    summary = pd.DataFrame(
        {
            "Metric": ["Total Students", "Attendance Rate", "Fee Collection", "Classes"],
            "Value": ["15,000", "96%", "87%", "24"]
        }
    )
    st.dataframe(summary, use_container_width=True, hide_index=True)
