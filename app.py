import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

def main():

    if "login_status" not in st.session_state:
        st.session_state["login_status"] = None

    match st.session_state["login_status"]:
        case "Teacher":
            teacher_screen()
        case "Student":
            student_screen()
        case None:
            home_screen()

main()