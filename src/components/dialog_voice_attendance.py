import streamlit as st
import pandas as pd

from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from src.components.dialog_attendance_results import show_attendance_result
from datetime import datetime


# ----------------------------------------
# Voice Attendance Dialog
# ----------------------------------------

@st.dialog('Voice Attendance')
def voice_attendance_dialog(selected_subject_id):

    # ----------------------------------------
    # Voice Attendance Instructions
    # ----------------------------------------

    st.write(
        'Record audio of students saying I am present. '
        'Then AI will recognize the students'
    )

    audio_data = None

    # ----------------------------------------
    # Record Classroom Audio
    # ----------------------------------------

    audio_data = st.audio_input("Record classroom audio")

    # ----------------------------------------
    # Analyze Audio
    # ----------------------------------------

    if st.button(
        'Analyze Audio',
        width='stretch',
        type='primary'
    ):

        # ----------------------------------------
        # Process Audio Data
        # ----------------------------------------

        with st.spinner('Prcessing Audio data'):

            # ----------------------------------------
            # Get Enrolled Students
            # ----------------------------------------

            try:
                enrolled_res = (
                    supabase
                    .table('subject_students')
                    .select("*, students(*)")
                    .eq('subject_id', selected_subject_id)
                    .execute()
                )

                enrolled_students = enrolled_res.data

            except Exception as e:
                st.error(
                    f"Unable to load enrolled students: {str(e)}"
                )
                return

            # ----------------------------------------
            # Check Enrolled Students
            # ----------------------------------------

            if not enrolled_students:
                st.warning(
                    'No students enrolled in this course'
                )
                return

            # ----------------------------------------
            # Get Students With Voice Profiles
            # ----------------------------------------

            try:
                candidates_dict = {
                    s['students']['student_id']:
                    s['students']['voice_embedding']
                    for s in enrolled_students
                    if s['students'].get('voice_embedding')
                }

            except Exception as e:
                st.error(
                    f"Unable to load student voice profiles: {str(e)}"
                )
                return

            # ----------------------------------------
            # Check Voice Profiles
            # ----------------------------------------

            if not candidates_dict:
                st.error(
                    'No enrolled students have voice profiles registerd'
                )
                return

            # ----------------------------------------
            # Check Audio Input
            # ----------------------------------------

            if audio_data is not None:

                try:
                    audio_bytes = audio_data.read()

                except Exception as e:
                    st.error(
                        f"Unable to read audio data: {str(e)}"
                    )
                    return

            else:
                st.warning(
                    "Please record or upload an audio file first."
                )
                return

            # ----------------------------------------
            # Process Voice Recognition
            # ----------------------------------------

            try:
                detected_scores = process_bulk_audio(
                    audio_bytes,
                    candidates_dict
                )

            except Exception as e:
                st.error(
                    f"Voice recognition failed: {str(e)}"
                )
                return

            # ----------------------------------------
            # Prepare Attendance Results
            # ----------------------------------------

            results, attendance_to_log = [], []

            current_timestamp = datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S"
            )

            # ----------------------------------------
            # Generate Student Attendance Results
            # ----------------------------------------

            try:

                for node in enrolled_students:

                    student = node['students']

                    score = detected_scores.get(
                        student['student_id'],
                        0.0
                    )

                    is_present = bool(score > 0)

                    results.append({
                        "Name": student['name'],
                        "ID": student['student_id'],
                        "Source": score if is_present else "-",
                        "Status": (
                            "✅ Present"
                            if is_present
                            else "❌ Absent"
                        )
                    })

                    attendance_to_log.append({
                        'student_id': student['student_id'],
                        'subject_id': selected_subject_id,
                        'timestamp': current_timestamp,
                        'is_present': bool(is_present)
                    })

            except Exception as e:
                st.error(
                    f"Unable to prepare attendance results: {str(e)}"
                )
                return

            # ----------------------------------------
            # Store Attendance Results
            # ----------------------------------------

            st.session_state.voice_attendance_results = (
                pd.DataFrame(results),
                attendance_to_log
            )

    # ----------------------------------------
    # Display Attendance Results
    # ----------------------------------------

    if st.session_state.get('voice_attendance_results'):

        st.divider()

        df_results, logs = (
            st.session_state.voice_attendance_results
        )

        show_attendance_result(
            df_results,
            logs
        )