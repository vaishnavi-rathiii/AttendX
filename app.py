import streamlit as st


# ============================================================
# SCREEN IMPORTS
# ============================================================

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    st.set_page_config(
        page_title="AttendX - AI Powered",
        page_icon="https://img.icons8.com/pulsar-color/1200/attendance-mark.jpg"
    )

    # ========================================================
    # INITIALIZE SESSION STATE
    # ========================================================

    if "login_status" not in st.session_state:
        st.session_state["login_status"] = None

    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

    if "is_logged_in" not in st.session_state:
        st.session_state["is_logged_in"] = False

    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None


    # ========================================================
    # READ JOIN CODE
    # ========================================================

    join_code = st.query_params.get("join-code")

    # If a join link was opened, remember that
    if join_code:

        st.session_state["join_code"] = join_code

        # Force student flow
        if st.session_state["login_status"] is None:
            st.session_state["login_type"] = "student"
            st.session_state["login_status"] = "Student"

            st.rerun()


    # ========================================================
    # MAIN APPLICATION FLOW
    # ========================================================

    match st.session_state["login_status"]:

        case "Teacher":
            teacher_screen()

        case "Student":
            student_screen()

        case None:
            home_screen()


    # ========================================================
    # AUTO ENROLLMENT
    # ========================================================

    stored_join_code = st.session_state.get("join_code")

    if (
        stored_join_code
        and st.session_state.get("is_logged_in")
        and st.session_state.get("user_role") == "student"
        and st.session_state.get("student_data")
    ):

        auto_enroll_dialog(stored_join_code)


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()