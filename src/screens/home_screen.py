import streamlit as st
from src.components.header import header_home
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home, style_background_dashboard


def home_screen():
    header_home()
    style_background_home()
    style_base_layout()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Teacher Portal"):
            st.session_state["login_status"] = "Teacher"

    with col2:
        if st.button("Student Portal"):
            st.session_state["login_status"] = "Student"