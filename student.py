import pandas as pd
import streamlit as st


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
            <h1>Student Profile</h1>
            <p>Secure personal record for your academic and administrative information.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-label'>Name</div>
                <div class='metric-value' style='font-size:1.4rem;'>{student['name']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-label'>Class</div>
                <div class='metric-value' style='font-size:1.4rem;'>{student['class_name']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-label'>Section</div>
                <div class='metric-value' style='font-size:1.4rem;'>{student['section']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-label'>Roll No</div>
                <div class='metric-value' style='font-size:1.4rem;'>{student['roll_number']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    profile = {
        "Full Name": student["name"],
        "Date of Birth": student["dob"],
        "Gender": student["gender"],
        "Email": student["email"],
        "Phone": student["phone"],
        "Address": student["address"],
        "Parent / Guardian": student["parent_name"],
        "Parent Phone": student["parent_phone"],
        "Class": student["class_name"],
        "Section": student["section"],
        "Username": student["username"],
    }

    st.markdown("<div class='section-title'>Student Information</div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(list(profile.items()), columns=["Field", "Value"]), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Academic Summary</div>", unsafe_allow_html=True)
    academic = pd.DataFrame(
        [
            {"Subject": "Mathematics", "Marks": "92", "Grade": "A+"},
            {"Subject": "Science", "Marks": "89", "Grade": "A"},
            {"Subject": "English", "Marks": "94", "Grade": "A+"},
            {"Subject": "Computer", "Marks": "96", "Grade": "A+"},
        ]
    )
    st.dataframe(academic, use_container_width=True, hide_index=True)
