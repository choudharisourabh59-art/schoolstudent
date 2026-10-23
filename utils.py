import streamlit as st


def show_success(message: str):
    st.markdown(f"<div class='alert-success'>{message}</div>", unsafe_allow_html=True)


def show_error(message: str):
    st.markdown(f"<div class='alert-error'>{message}</div>", unsafe_allow_html=True)


def metric_box(title: str, value: str, color=None):
    if color:
        color_style = f"color: {color};"
    else:
        color_style = ""
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-label'>{title}</div>
            <div class='metric-value' style='{color_style}'>{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
