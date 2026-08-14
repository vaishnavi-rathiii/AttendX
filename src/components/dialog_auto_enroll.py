import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

import time


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):

    # ----------------------------------------
    # Get logged-in student
    # ----------------------------------------

    student_data = st.session_state.get("student_data")

    if not student_data:
        st.error("Student information not found.")
        return

    student_id = student_data.get("student_id")

    if not student_id:
        st.error("Student ID not found.")
        return

    # ----------------------------------------
    # Find subject
    # ----------------------------------------

    try:

        res = (
            supabase
            .table("subjects")
            .select("subject_id, name")
            .eq("subject_code", subject_code)
            .execute()
        )

    except Exception as e:

        st.error(f"Unable to find subject: {e}")
        return

    if not res.data:

        st.error("Subject Code not found!")

        if st.button("Close"):
            st.query_params.clear()
            st.session_state.pop("join_code", None)
            st.rerun()

        return

    subject = res.data[0]

    # ----------------------------------------
    # Check existing enrollment
    # ----------------------------------------

    check = (
        supabase
        .table("subject_students")
        .select("*")
        .eq("subject_id", subject["subject_id"])
        .eq("student_id", student_id)
        .execute()
    )

    if check.data:

        st.info("You're already enrolled!")

        if st.button("Got it!"):
            st.query_params.clear()
            st.session_state.pop("join_code", None)
            st.rerun()

        return

    # ----------------------------------------
    # Enrollment confirmation
    # ----------------------------------------

    st.markdown(
        f"Would you like to enroll in **{subject['name']}**?"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("No thanks"):

            st.query_params.clear()
            st.session_state.pop("join_code", None)
            st.rerun()

    with col2:

        if st.button(
            "Yes, enroll now!",
            type="primary",
            width="stretch"
        ):

            try:

                enroll_student_to_subject(
                    student_id,
                    subject["subject_id"]
                )

                st.success("Joined successfully!")

                st.query_params.clear()
                st.session_state.pop("join_code", None)

                time.sleep(1)

                st.rerun()

            except Exception as e:

                st.error(f"Enrollment failed: {e}")