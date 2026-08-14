import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog

from src.database.config import supabase
from src.database.db import (
    check_teacher_exists, 
    create_teacher, 
    teacher_login, 
    get_teacher_subjects, 
    get_attendance_for_teacher
)

from src.pipelines.face_pipeline import predict_attendance


# ============================================================
# DASHBOARD BUTTON STYLING
# ============================================================


def style_dashboard_buttons():
    """Cohesive green palette — each button a distinct shade, all in the green family."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&display=swap');

        /* Shared base: rounded, soft shadow, gentle lift on hover for every button */
        [data-testid="stButton"] button,
        [data-testid="stBaseButton-primary"],
        [data-testid="stBaseButton-secondary"],
        [data-testid="stBaseButton-tertiary"] {
            border-radius: 12px !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
            transition: transform 0.12s ease, box-shadow 0.12s ease, background-color 0.15s ease !important;
        }
        [data-testid="stButton"] button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 14px rgba(0, 0, 0, 0.15) !important;
        }
        [data-testid="stButton"] button:active {
            transform: translateY(0);
        }

        /* ---- Fallback type-based defaults ---- */
        [data-testid="stBaseButton-primary"] {
            background-color: #1B5E4B !important;
            color: white !important;
            border: none !important;
        }
        [data-testid="stBaseButton-primary"]:hover { background-color: #0F3D30 !important; color: white !important; }

        [data-testid="stBaseButton-secondary"] {
            background-color: #4C7A63 !important;
            color: #ffffff !important;
            border: 1.5px solid #3B6250 !important;
        }
        [data-testid="stBaseButton-secondary"]:hover { background-color: #3B6250 !important; }

        [data-testid="stBaseButton-tertiary"] {
            background-color: #A8D5BE !important;
            color: #14432F !important;
            border: none !important;
        }
        [data-testid="stBaseButton-tertiary"]:hover { background-color: #86C0A2 !important; }

        /* ---- Per-button colors, keyed to each st.container(key=...) ---- */
        /* NOTE: text lives in nested <p>/<div>/<span> inside the button, so every
           rule below also targets `button *` to force the text color, not just
           the button background — otherwise text can inherit white-on-white. */

        /* Nav tabs (active state still uses primary dark green above via type="primary") */
        .st-key-nav_take_attendance button,
        .st-key-nav_manage_subjects button,
        .st-key-nav_attendance_records button {
            background-color: #4F9D77 !important;
            border: 1.5px solid #3C7C5D !important;
        }
        .st-key-nav_take_attendance button *,
        .st-key-nav_manage_subjects button *,
        .st-key-nav_attendance_records button * {
            color: #ffffff !important;
        }
        .st-key-nav_take_attendance button:hover,
        .st-key-nav_manage_subjects button:hover,
        .st-key-nav_attendance_records button:hover {
            background-color: #3C7C5D !important;
        }

        /* Logout — deep pine green, still clearly "exit" within the green family */
        .st-key-loginbackbtn button {
            background-color: #14532D !important;
            border: 1.5px solid #0C3A1F !important;
        }
        .st-key-loginbackbtn button * { color: #ffffff !important; }
        .st-key-loginbackbtn button:hover { background-color: #0C3A1F !important; }

        /* Add Photos — bright emerald, inviting/creative action */
        .st-key-addphotosbtn button {
            background-color: #059669 !important;
            border: none !important;
        }
        .st-key-addphotosbtn button * { color: #ffffff !important; }
        .st-key-addphotosbtn button:hover { background-color: #047857 !important; }

        /* Clear all photos — muted sage green, low-emphasis destructive */
        .st-key-clearphotosbtn button {
            background-color: #7A9A83 !important;
            border: 1.5px solid #5F7A67 !important;
        }
        .st-key-clearphotosbtn button * { color: #ffffff !important; }
        .st-key-clearphotosbtn button:hover { background-color: #5F7A67 !important; }

        /* Run Face Analysis — deep teal-green, main AI action */
        .st-key-runanalysisbtn button {
            background-color: #0F766E !important;
            border: none !important;
        }
        .st-key-runanalysisbtn button * { color: #ffffff !important; }
        .st-key-runanalysisbtn button:hover { background-color: #0B5C55 !important; }

        /* Use Voice Attendance — vivid grass green, distinct feature */
        .st-key-voiceattendancebtn button {
            background-color: #16A34A !important;
            border: none !important;
        }
        .st-key-voiceattendancebtn button * { color: #ffffff !important; }
        .st-key-voiceattendancebtn button:hover { background-color: #15803D !important; }

        /* Create New Subject — dark jade, positive/creation action */
        .st-key-createsubjectbtn button {
            background-color: #065F46 !important;
            border: none !important;
        }
        .st-key-createsubjectbtn button * { color: #ffffff !important; }
        .st-key-createsubjectbtn button:hover { background-color: #064E3B !important; }

        /* Disabled state: explicit muted-gray style with dark, readable text —
           NOT a plain opacity fade, since fading white text on a colored button
           washes both toward the page background and kills contrast. */
        [data-testid="stButton"] button:disabled {
            opacity: 1 !important;
            background-color: #D1D5DB !important;
            border: 1.5px solid #9CA3AF !important;
            box-shadow: none !important;
            cursor: not-allowed !important;
        }
        [data-testid="stButton"] button:disabled * {
            color: #374151 !important;
        }
        [data-testid="stButton"] button:disabled:hover {
            transform: none !important;
            box-shadow: none !important;
        }

        /* Keep all section headings on a consistent font */
        [data-testid="stHeading"] h1,
        [data-testid="stHeading"] h2,
        [data-testid="stHeading"] h3 {
            font-family: "Playfair Display", serif !important;
            font-weight: 600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TEACHER SCREEN
# ============================================================


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
        return

    if "teacher_login_status" not in st.session_state:
        st.session_state.teacher_login_status = "Login"

    if st.session_state.teacher_login_status == "Login":
        teacher_screen_login()

    elif st.session_state.teacher_login_status == "Register":
        teacher_screen_register()


# ============================================================
# TEACHER DASHBOARD
# ============================================================


def teacher_dashboard():
    style_dashboard_buttons()

    teacher_data = st.session_state.teacher_data

    c1, c2 = st.columns([1.3, 0.9], vertical_alignment="center")
    
    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"Welcome, {teacher_data['name']}")
        with st.container(key="loginbackbtn"):
            if st.button(
                "Logout",
                type="secondary",
                key="loginbackbtn_widget",
                shortcut="control+backspace",
                width=260
            ):
                st.session_state["is_logged_in"] = False
                del st.session_state.teacher_data
                st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
        with st.container(key="nav_take_attendance"):
            if st.button("Take Attendance", type=type1, width="stretch"):
                st.session_state.current_teacher_tab = "take_attendance"
                st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"
        with st.container(key="nav_manage_subjects"):
            if st.button("Manage Subjects", type=type2, width="stretch"):
                st.session_state.current_teacher_tab = "manage_subjects"
                st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "tertiary"
        with st.container(key="nav_attendance_records"):
            if st.button("Attendance Records", type=type3, width="stretch"):
                st.session_state.current_teacher_tab = "attendance_records"
                st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()


# ============================================================
# TAKE ATTENDANCE TAB
# ============================================================


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return
    
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        with st.container(key="addphotosbtn"):
            if st.button('Add Photos', type='primary', width='stretch'):
                add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(key="clearphotosbtn"):
            if st.button('Clear all photos', width='stretch', type='tertiary', disabled=not has_photos):
                st.session_state.attendance_images = []
                st.rerun()


    with c2:
        run_analysis_container = st.container(key="runanalysisbtn")
        with run_analysis_container:
            run_clicked = st.button('Run Face Analysis', width='stretch', type='secondary', disabled=not has_photos)

        if run_clicked:
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)


                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id',selected_subject_id ).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:

                    results, attendance_to_log  = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present= len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        with st.container(key="voiceattendancebtn"):
            if st.button('Use Voice Attendance', type='primary', width='stretch'):
                voice_attendance_dialog(selected_subject_id)

    footer_dashboard()

# ============================================================
# MANAGE SUBJECTS TAB
# ============================================================


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header("Manage Subjects")

    with col2:
        st.markdown(
            "<div style='height: 25px; margin-left: 50px !important;'></div>",
            unsafe_allow_html=True
        )

        with st.container(key="createsubjectbtn"):
            if st.button("Create New Subject", width=270):
                create_subject_dialog(teacher_id)

        # st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # List all Subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]
        def share_btn():
            if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}"):
                share_subject_dialog(sub['name'], sub['subject_code'])
            st.space()

        subject_card(
            name = sub['name'],
            code = sub['subject_code'],
            section = sub['section'],
            stats=stats,
            footer_callback=share_btn
        )
    else:
        st.info("Subjects NOT Found. Create one above")

    footer_dashboard()

# ============================================================
# ATTENDANCE RECORDS TAB
# ============================================================


def teacher_tab_attendance_records():
    st.header('Attendance Records')

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return
    
    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
            "Subject": r['subjects']['name'],
            "Subject Code":r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })


    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count = ('is_present', 'sum'),
            Total_Count =('is_present', 'count')
        ).reset_index()

    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = ( summary.sort_values(by='ts_group' ,ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
                  )
    
    st.dataframe(display_df, width='stretch', hide_index=True)


    footer_dashboard()


# ============================================================
# LOGIN SCREEN
# ============================================================

# ============================================================
# LOGIN FUNCTIONS
# ============================================================


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False 

# ============================================================
# TEACHER LOGIN
# ============================================================


def teacher_screen_login():

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined');

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

    c1, c2 = st.columns([1.3, 0.9], vertical_alignment="center")

    with c1:
        header_dashboard()

    with c2:
        with st.container(key="loginbackbtn"):
            if st.button(
                "Go Back to Home",
                type="secondary",
                key="loginbackbtn_widget",
                shortcut="control+backspace",
                width=260
            ):
                # st.session_state.teacher_login_status = "Login"
                st.session_state["login_status"] = None
                st.rerun()

    st.markdown(
        '<div class="login-title">Login using Password</div>',
        unsafe_allow_html=True
    )

    _, form, _ = st.columns([1, 3, 1])

    with form:

        st.text_input(
            "Enter your Username :",
            key="teacher_username",
            placeholder="Enter your email"
        )

        if "show_teacher_login_password" not in st.session_state:
            st.session_state.show_teacher_login_password = False

        password_type = "default" if st.session_state.show_teacher_login_password else "password"

        st.text_input(
            "Enter your Password :",
            key="teacher_password",
            placeholder="Enter your password",
            type=password_type
        )

        if st.button(
            "visibility_off" if st.session_state.show_teacher_login_password else "visibility",
            key="teacher_login_eye",
            help="Show / Hide Password"
        ):
            st.session_state.show_teacher_login_password = not st.session_state.show_teacher_login_password
            st.rerun()

    st.divider()

    _, b1, _, b2, _ = st.columns([1.5, 1, 0.35, 1, 1.5])

    with b1:
        with st.container(key="loginsubmitbtn"):
            if st.button(
                "Login",
                key="loginsubmitbtn_widget",
                shortcut="control+enter",
                width=320
            ):
                if login_teacher(
                    st.session_state.teacher_username,
                    st.session_state.teacher_password
                ):
                    st.toast("Welcome Back!", icon="👋")
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid Username & Password Combo.")

    with b2:
        with st.container(key="logingotoregisterbtn"):
            if st.button(
                "Register Instead",
                type="primary",
                key="logingotoregisterbtn_widget",
                width=240
            ):
                st.session_state.teacher_login_status = "Register"
                st.rerun()

    footer_dashboard()


# ============================================================
# REGISTRATION SCREEN
# ============================================================

# ============================================================
# REGISTRATION FUNCTIONS
# ============================================================


def register_teacher(
    teacher_username,
    teacher_name,
    teacher_pass,
    teacher_pass_confirm
):
    if not teacher_username or not teacher_name or not teacher_pass or not teacher_pass_confirm:
        return False, "All Fields are Required!"

    if check_teacher_exists(teacher_username):
        return False, "Username Already Taken"

    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match."

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Successfully Created! Login Now."
    except Exception as e:
        # return False, "UnExpected Error!"
        return False, str(e)


# ============================================================
# TEACHER REGISTRATION
# ============================================================


def teacher_screen_register():

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined');

        [data-testid="stMainBlockContainer"] {
            max-width: 900px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        .register-title {
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

        .st-key-registerbackbtn button {
            padding-left: 20px !important;
            padding-right: 20px !important;
        }

        .st-key-registersubmitbtn button {
            padding-left: 7px !important;
            padding-right: 40px !important;
            min-width: 300px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 14px !important;
        }

        .st-key-registergotologinbtn button {
            padding-left: 20px !important;
            padding-right: 20px !important;
        }

        /* Hide Streamlit's default password eye */
        button[data-testid="stTextInputRevealButton"] {
            display: none !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns([1.3, 0.9], vertical_alignment="center")

    with c1:
        header_dashboard()

    with c2:
        with st.container(key="registerbackbtn"):
            if st.button(
                "Go Back to Home",
                type="secondary",
                key="registerbackbtn_widget",
                shortcut="control+backspace",
                width=260
            ):
                st.session_state.teacher_login_status = "Login"
                st.rerun()

    st.markdown(
        '<div class="register-title">Register your Teacher Profile</div>',
        unsafe_allow_html=True
    )

    _, form, _ = st.columns([1, 3, 1])

    with form:

        st.text_input(
            "Enter your Username :",
            key="register_teacher_username",
            placeholder="Enter your email"
        )

        st.text_input(
            "Enter Name :",
            key="teacher_name",
            placeholder="Enter your full name"
        )

        if "show_register_password" not in st.session_state:
            st.session_state.show_register_password = False

        register_password_type = (
            "default"
            if st.session_state.show_register_password
            else "password"
        )

        st.text_input(
            "Enter your Password :",
            key="register_teacher_password",
            placeholder="Create a password",
            type=register_password_type
        )

        if st.button(
            "visibility_off" if st.session_state.show_register_password else "visibility",
            key="register_password_eye",
            help="Show / Hide Password"
        ):
            st.session_state.show_register_password = not st.session_state.show_register_password
            st.rerun()

        if "show_confirm_password" not in st.session_state:
            st.session_state.show_confirm_password = False

        confirm_password_type = (
            "default"
            if st.session_state.show_confirm_password
            else "password"
        )

        st.text_input(
            "Confirm your Password :",
            key="teacher_password_confirm",
            placeholder="Re-enter your password",
            type=confirm_password_type
        )

        if st.button(
            "visibility_off" if st.session_state.show_confirm_password else "visibility",
            key="confirm_password_eye",
            help="Show / Hide Password"
        ):
            st.session_state.show_confirm_password = not st.session_state.show_confirm_password
            st.rerun()

    st.divider()

    _, b1, _, b2, _ = st.columns([1.5, 1, 0.35, 1, 1.5])

    with b1:
        with st.container(key="registersubmitbtn"):
            if st.button(
                "Register Now",
                key="registersubmitbtn_widget",
                shortcut="control+enter",
                width=320
            ):
                success, message = register_teacher(
                    st.session_state.register_teacher_username,
                    st.session_state.teacher_name,
                    st.session_state.register_teacher_password,
                    st.session_state.teacher_password_confirm
                )

                if success:
                    st.success(message)
                    import time
                    time.sleep(2)
                    st.session_state.teacher_login_status = "Login"
                    st.rerun()
                else:
                    st.error(message)

    with b2:
        with st.container(key="registergotologinbtn"):
            if st.button(
                "Login Instead",
                type="primary",
                key="registergotologinbtn_widget",
                width=240
            ):
                st.session_state.teacher_login_status = "Login"
                st.rerun()

    footer_dashboard()