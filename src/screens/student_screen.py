import streamlit as st
import numpy as np

# ============================================================
# UI COMPONENTS
# ============================================================

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject
)


# ============================================================
# AI PIPELINES
# ============================================================

from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier
)

from src.pipelines.voice_pipeline import get_voice_embedding


# ============================================================
# EXTERNAL LIBRARIES
# ============================================================

from PIL import Image


# ============================================================
# STUDENT DASHBOARD
# ============================================================

def student_dashboard():

    # ========================================================
    # STUDENT SESSION DATA
    # ========================================================

    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    # ========================================================
    # DASHBOARD HEADER
    # ========================================================

    c1, c2 = st.columns(
        2,
        vertical_alignment='center',
        gap='xxlarge'
    )

    with c1:
        header_dashboard()

    with c2:

        st.subheader(
            f"""Welcome, {student_data['name']} """
        )

        # ====================================================
        # LOGOUT BUTTON STYLING
        # ====================================================

        with c2:

            st.markdown(
                """
                <style>

                /* Logout button */
                .st-key-logout_btn button {
                    width: 250px !important;
                    margin-left: 0px !important;
                    height: 50px !important;
                }

                </style>
                """,
                unsafe_allow_html=True
            )

            # =================================================
            # LOGOUT BUTTON
            # =================================================

            if st.button(
                "Logout",
                type="primary",
                key="logout_btn"
            ):

                st.session_state['is_logged_in'] = False
                st.session_state.pop('student_data', None)
                st.rerun()

    # ============================================================
    # SUBJECT SECTION
    # ============================================================

    st.space()

    c1, c2 = st.columns(2)

    with c1:

        st.header(
            'Your Enrolled Subjects'
        )

    with c2:

        # ========================================================
        # ENROLL BUTTON STYLING
        # ========================================================

        st.markdown(
            """
            <style>

            /* Enroll button */
            .st-key-enroll_subject_btn button {
                width: 250px !important;
                margin-left: 55px !important;
                height: 50px !important;
                margin-top: 5px !important;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

        # ========================================================
        # ENROLL BUTTON
        # ========================================================

        if st.button(
            "Enroll in Subject",
            type="primary",
            key="enroll_subject_btn"
        ):

            enroll_dialog()

    # ============================================================
    # LOAD STUDENT DATA
    # ============================================================

    st.divider()

    with st.spinner(
        'Loading your enrolled subjects..'
    ):

        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    # ============================================================
    # CALCULATE ATTENDANCE STATISTICS
    # ============================================================

    stats_map = {}

    for log in logs:

        sid = log['subject_id']

        if sid not in stats_map:

            stats_map[sid] = {
                "total": 0,
                "attended": 0
            }

        stats_map[sid]['total'] += 1

        if log.get('is_present'):

            stats_map[sid]['attended'] += 1

    # ============================================================
    # DISPLAY ENROLLED SUBJECTS
    # ============================================================

    cols = st.columns(2)

    for i, sub_node in enumerate(subjects):

        # ========================================================
        # SUBJECT DATA
        # ========================================================

        sub = sub_node['subjects']
        sid = sub['subject_id']

        stats = stats_map.get(
            sid,
            {
                "total": 0,
                "attended": 0
            }
        )

        # ========================================================
        # UNENROLL FUNCTION
        # ========================================================

        def unenroll_button():

            if st.button(
                "Unenroll from this course",
                type='tertiary',
                width="stretch"
            ):

                unenroll_student_to_subject(
                    student_id,
                    sid
                )

                st.toast(
                    f"Unenrolled from {sub['name']} successfully!"
                )

                st.rerun()

        # ========================================================
        # SUBJECT CARD
        # ========================================================

        with cols[i % 2]:

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )

    # ============================================================
    # FOOTER
    # ============================================================

    footer_dashboard()


# ============================================================
# STUDENT LOGIN / REGISTRATION SCREEN
# ============================================================

def student_screen():

    # ============================================================
    # BASE LAYOUT
    # ============================================================

    style_background_dashboard()
    style_base_layout()

    # ============================================================
    # GLOBAL PAGE STYLING
    # ============================================================

    st.markdown(
        """
        <style>

        @import url(
            'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined'
        );

        [data-testid="stMainBlockContainer"] {
            max-width: 900px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        .login-title {
            font-family: "Playfair Display", serif;
            font-size: 38px;
            font-weight: 600;
            color: #1B5E4B;
            text-align: center;
            margin-top: 55px;
            margin-bottom: 70px;
        }

        [data-testid="stButton"] button {
            white-space: nowrap !important;
        }

        [data-testid="stButton"] button p,
        [data-testid="stButton"] button span {
            white-space: nowrap !important;
        }

        .st-key-loginbackbtn button {
            padding-left: 20px !important;
            padding-right: 20px !important;
        }

        .st-key-loginsubmitbtn button {
            padding-left: 40px !important;
            padding-right: 40px !important;
            min-width: 300px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 14px !important;
        }

        .st-key-logingotoregisterbtn button {
            padding-left: 20px !important;
            padding-right: 20px !important;
        }

        /* Hide Streamlit's default password eye */
        button[data-testid="stTextInputRevealButton"] {
            display: none !important;
        }

        .password-row {
            display: flex;
            align-items: center;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ============================================================
    # STUDENT DASHBOARD
    # ============================================================

    if "student_data" in st.session_state:

        student_dashboard()
        return

    # ============================================================
    # HEADER
    # ============================================================

    c1, c2 = st.columns(
        [1.3, 0.9],
        vertical_alignment="center"
    )

    with c1:

        header_dashboard()

    with c2:

        with st.container(
            key="loginbackbtn"
        ):

            # ====================================================
            # GO BACK TO HOME BUTTON
            # ====================================================

            if st.button(
                "Go Back to Home",
                type="secondary",
                key="student_go_home",
                width=260
            ):

                st.session_state["login_status"] = None
                st.session_state["login_type"] = None
                st.session_state["is_logged_in"] = False
                st.session_state["user_role"] = None

                st.session_state.pop(
                    "student_data",
                    None
                )

                st.session_state.pop(
                    "join_code",
                    None
                )

                st.query_params.clear()

                st.rerun()

    # ============================================================
    # FACE ID STYLING
    # ============================================================

    st.markdown(
        """
        <style>

        .faceid-title {
            font-family: "Playfair Display", serif;
            font-size: 38px;
            font-weight: 600;
            color: #1B5E4B;
            text-align: center;
            margin-top: 10px;
            margin-bottom: 12px;
        }

        .camera-instruction {
            font-family: "Playfair Display", serif;
            font-size: 20px;
            font-weight: 500;
            color: #1B5E4B;
            text-align: center;
            margin-top: 0px;
            margin-bottom: 18px;
        }

        [data-testid="stCameraInput"] {
            width: 800px !important;
            margin: 0 auto !important;
        }

        [data-testid="stCameraInput"] button {
            background-color: #1B5E4B !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 30px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            min-width: 220px !important;
        }

        [data-testid="stCameraInput"] button:hover {
            background-color: #164C3D !important;
            color: white !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ============================================================
    # FACE ID TITLE
    # ============================================================

    st.markdown(
        '<div class="faceid-title">Login using FaceID</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="camera-instruction">Position your Face in center</div>',
        unsafe_allow_html=True
    )

    # ============================================================
    # REGISTRATION STATE
    # ============================================================

    if "show_student_registration" not in st.session_state:

        st.session_state.show_student_registration = False

    # ============================================================
    # CAMERA INPUT
    # ============================================================

    photo_source = st.camera_input(
        "",
        label_visibility="collapsed"
    )

    # ============================================================
    # FACE RECOGNITION
    # ============================================================

    if photo_source:

        img = np.array(
            Image.open(photo_source)
        )

        with st.spinner(
            "AI is Scanning..."
        ):

            detected, all_ids, num_faces = predict_attendance(img)

            # ====================================================
            # NO FACE DETECTED
            # ====================================================

            if num_faces == 0:

                st.warning(
                    "Face NOT Found!"
                )

                st.session_state.show_student_registration = True

            # ====================================================
            # MULTIPLE FACES DETECTED
            # ====================================================

            elif num_faces > 1:

                st.warning(
                    "Multiple Faces Found."
                )

                st.session_state.show_student_registration = False

            # ====================================================
            # EXACTLY ONE FACE DETECTED
            # ============================================================

            else:

                # =================================================
                # KNOWN STUDENT
                # =================================================

                if detected:

                    student_id = list(
                        detected.keys()
                    )[0]

                    all_students = get_all_students()

                    student = next(
                        (
                            s
                            for s in all_students
                            if s["student_id"] == student_id
                        ),
                        None
                    )

                    # =============================================
                    # STUDENT FOUND
                    # =============================================

                    if student:

                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student
                        st.session_state["login_status"] = "Student"

                        st.session_state.show_student_registration = False

                        st.toast(
                            f"Welcome Back {student['name']}"
                        )

                        import time

                        time.sleep(1)

                        st.rerun()

                # =================================================
                # UNKNOWN STUDENT
                # =================================================

                else:

                    st.info(
                        "Face NOT Recognized! "
                        "You might be a NEW Student."
                    )

                    st.session_state.show_student_registration = True

    # ============================================================
    # NEW STUDENT REGISTRATION
    # ============================================================

    if st.session_state.show_student_registration:

        with st.container(
            border=True
        ):

            # ====================================================
            # REGISTRATION HEADER
            # ====================================================

            st.header(
                "Register NEW Profile"
            )

            # ====================================================
            # STUDENT NAME
            # ====================================================

            new_name = st.text_input(
                "Enter your Name :",
                placeholder="Eg: ABC"
            )

            # ====================================================
            # VOICE ENROLLMENT
            # ====================================================

            st.subheader(
                "Optional : Voice Enrollment"
            )

            st.info(
                "Enroll your voice for voice-only attendance."
            )

            audio_data = None

            try:

                audio_data = st.audio_input(
                    "Record a short phrase like: "
                    "I'm present, my name is ABC."
                )

            except Exception:

                st.error(
                    "Audio Data Failed!"
                )

            # ====================================================
            # CREATE ACCOUNT
            # ====================================================

            if st.button(
                "Create Account",
                type="primary"
            ):

                if new_name:

                    with st.spinner(
                        "Creating Profile..."
                    ):

                        img = np.array(
                            Image.open(photo_source)
                        )

                        encodings = get_face_embeddings(
                            img
                        )

                        # ========================================
                        # FACE EMBEDDING FOUND
                        # ========================================

                        if encodings:

                            faceEmbedding = (
                                encodings[0].tolist()
                            )

                            voiceEmbedding = None

                            # ====================================
                            # VOICE EMBEDDING
                            # ====================================

                            if audio_data:

                                voiceEmbedding = (
                                    get_voice_embedding(
                                        audio_data.read()
                                    )
                                )

                            # ========================================
                            # CREATE STUDENT
                            # ========================================

                            response_data = create_student(
                                new_name,
                                face_embedding=faceEmbedding,
                                voice_embedding=voiceEmbedding
                            )

                            # ========================================
                            # ACCOUNT CREATED
                            # ========================================

                            if response_data:

                                train_classifier()

                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response_data[0]
                                st.session_state["login_status"] = "Student"

                                st.session_state.show_student_registration = False

                                st.toast(
                                    f"Profile created, Hi {new_name}!"
                                )

                                import time

                                time.sleep(1)

                                st.rerun()

                            else:

                                st.error(
                                    "Couldn't create your profile."
                                )

                        # ========================================
                        # FACE NOT FOUND
                        # ========================================

                        else:

                            st.error(
                                "No face detected. "
                                "Please capture your photo again."
                            )

                else:

                    st.warning(
                        "Please Enter your name!"
                    )

    # ============================================================
    # FOOTER
    # ============================================================

    footer_dashboard()