import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.teacher_dashboard import teacher_dashboard
from src.screens.student_dashboard import student_dashboard
from src.screens.teacher_login import teacher_login
from src.components.auto_enroll_dialog import auto_enroll_dialog
from src.components.ui_styles import inject_global_css
from PIL import Image


def main():
    inject_global_css()
    logo = Image.open("assets/logo.png")

    st.set_page_config(
        page_title='SmartAttend - Making Attendance Faster with Automated Recognition',
        page_icon=logo
    )
    
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    join_code = st.query_params.get('subject_code')
    
    if join_code:
        if st.session_state.get('login_type') != 'student':
            st.session_state['login_type'] = 'student'
            st.rerun()

    match st.session_state.get('login_type'):
        case 'teacher':
            teacher_dashboard()
        case 'teacher_login':
            teacher_login()
        case 'student':
            student_dashboard()
        case _:
            home_screen()

    if join_code:
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)

if __name__ == "__main__":
    main()