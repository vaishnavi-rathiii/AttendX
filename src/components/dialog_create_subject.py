import streamlit as st
from src.database.db import create_subject


# ----------------------------------------
# Create Subject Dialog
# ----------------------------------------

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):

    # ----------------------------------------
    # Subject Details
    # ----------------------------------------

    st.write("Enter the details of new subject")

    sub_id = st.text_input(
        "Subject Code",
        placeholder="AN101"
    )

    sub_name = st.text_input(
        "Subject Name",
        placeholder="Intro to DSA"
    )

    sub_section = st.text_input(
        "Section",
        placeholder="A"
    )

    # ----------------------------------------
    # Create Subject
    # ----------------------------------------

    if st.button(
        "Create Subject Now",
        type='primary',
        width='stretch'
    ):

        # ----------------------------------------
        # Validate Input
        # ----------------------------------------

        if sub_id and sub_name and sub_section:

            # ----------------------------------------
            # Create Subject in Database
            # ----------------------------------------

            try:
                create_subject(
                    sub_id,
                    sub_name,
                    sub_section,
                    teacher_id
                )

                st.toast("Subject Created Succesfully!")
                st.rerun()

            except Exception as e:

                # ----------------------------------------
                # Handle Database Error
                # ----------------------------------------

                st.error(f"Error: {str(e)}")

        else:

            # ----------------------------------------
            # Handle Missing Input
            # ----------------------------------------

            st.warning("Please fill all the fields")