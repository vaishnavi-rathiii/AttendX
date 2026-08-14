import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home


# ----------------------------------------
# Home Screen
# ----------------------------------------

def home_screen():

    # ----------------------------------------
    # Apply Home Page Styling
    # ----------------------------------------

    style_background_home()
    style_base_layout()

    # ----------------------------------------
    # Display Home Header
    # ----------------------------------------

    header_home()

    # ----------------------------------------
    # Create Teacher and Student Columns
    # ----------------------------------------

    col1, col2 = st.columns(2, gap="large")

    # ----------------------------------------
    # Teacher Portal
    # ----------------------------------------

    with col1:

        st.header("I'm Teacher")

        st.image(
            "https://i.ibb.co/CsmQQV6X/mascot-prof.png",
            width=150
        )

        if st.button(
            "Teacher Portal ↗",
            type="primary"
        ):

            # Set login status to Teacher
            st.session_state["login_status"] = "Teacher"

    # ----------------------------------------
    # Student Portal
    # ----------------------------------------

    with col2:

        st.header("I'm Student")

        st.image(
            "https://i.ibb.co/844D9Lrt/mascot-student.png",
            width=125
        )

        if st.button(
            "Student Portal ↗",
            type="primary"
        ):

            # Set login status to Student
            st.session_state["login_status"] = "Student"

            # Refresh the application
            st.rerun()

    # ----------------------------------------
    # Display Home Footer
    # ----------------------------------------

    footer_home()