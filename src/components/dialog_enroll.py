import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

import time


# ----------------------------------------
# Enroll in Subject Dialog
# ----------------------------------------

@st.dialog("Enroll in Subject")
def enroll_dialog():

    # ----------------------------------------
    # Subject Code Input
    # ----------------------------------------

    st.write('Enter the subject code provided by your teacher to enroll')

    join_code = st.text_input(
        'Subject Code',
        placeholder='Eg. CS101'
    )

    # ----------------------------------------
    # Enroll Button
    # ----------------------------------------

    if st.button(
        'Enroll now',
        type='primary',
        width='stretch'
    ):

        # ----------------------------------------
        # Validate Subject Code
        # ----------------------------------------

        if join_code:

            # ----------------------------------------
            # Find Subject
            # ----------------------------------------

            try:
                res = (
                    supabase
                    .table('subjects')
                    .select('subject_id, name, subject_code')
                    .eq('subject_code', join_code)
                    .execute()
                )

            except Exception as e:
                st.error(f"Unable to find subject: {str(e)}")
                return

            # ----------------------------------------
            # Check Subject
            # ----------------------------------------

            if res.data:

                subject = res.data[0]

                # Get the logged-in student's ID
                student_id = st.session_state.student_data['student_id']

                # ----------------------------------------
                # Check Existing Enrollment
                # ----------------------------------------

                try:
                    check = (
                        supabase
                        .table('subject_students')
                        .select('*')
                        .eq('subject_id', subject['subject_id'])
                        .eq('student_id', student_id)
                        .execute()
                    )

                except Exception as e:
                    st.error(f"Unable to check enrollment: {str(e)}")
                    return

                # ----------------------------------------
                # Enrollment Status
                # ----------------------------------------

                if check.data:

                    st.warning(
                        'You are already enrolled in this program'
                    )

                else:

                    # ----------------------------------------
                    # Enroll Student
                    # ----------------------------------------

                    try:
                        enroll_student_to_subject(
                            student_id,
                            subject['subject_id']
                        )

                        st.success('Succesfully enrolled!')

                        time.sleep(1)
                        st.rerun()

                    except Exception as e:
                        st.error(
                            f"Enrollment failed: {str(e)}"
                        )

            else:

                # ----------------------------------------
                # Subject Not Found
                # ----------------------------------------

                st.error('Subject Code not found')

        else:

            # ----------------------------------------
            # Missing Subject Code
            # ----------------------------------------

            st.warning('Please enter a subject code')