from time import time

import streamlit as st
from textwrap import dedent
from src.components.header import global_header
from src.database.db import check_teacher_exists, create_teacher,teacher_login_check

def teacher_login():
    if "teacher_auth_mode" not in st.session_state:
        st.session_state.teacher_auth_mode = "login"

    global_header(show_auth=False, portal_type="Teacher Portal")
    def register_teacher(username, password, name):
        if check_teacher_exists(username):
            return False, "Username already exists. Please choose a different one."
        else:
            try:
                create_teacher(username, password, name)
                return True, "Teacher registered successfully."
            except Exception as e:
                return False, f'Error registering teacher: {str(e)}'

    if st.session_state.teacher_auth_mode == "login":
        with st.form("teacher_login_form", clear_on_submit=False):
            st.markdown(dedent("""
            <div style="display: flex; justify-content: center; margin-bottom: 16px;">
                <div style="background: rgba(245,158,11,0.15); width: 64px; height: 64px; border-radius: 18px; display: flex; align-items: center; justify-content: center; font-size: 28px; box-shadow: 0 4px 12px rgba(245,158,11,0.1);">
                    👩‍🏫
                </div>
            </div>
            <div class="form-title">Welcome Back</div>
            <div class="form-subtitle">Login to your Teacher Portal to manage attendance.</div>
            """), unsafe_allow_html=True)

            st.markdown('<div class="input-label">Username</div>', unsafe_allow_html=True)
            username = st.text_input(
                "Username",
                placeholder="@username",
                label_visibility="collapsed",
                key="login_username"
            )

            st.markdown('<div class="input-label">Password</div>', unsafe_allow_html=True)
            password = st.text_input(
                "Password",
                placeholder="Enter password",
                type="password",
                label_visibility="collapsed",
                key="login_password"
            )

            st.write("")

            btn_col1, btn_col2 = st.columns(2, gap="small")

            with btn_col1:
                login_btn = st.form_submit_button("Login", use_container_width=True)

            with btn_col2:
                switch_register = st.form_submit_button("Create Account", use_container_width=True)

        if login_btn:
            if username and password:
                if check_teacher_exists(username):
                    teacher = teacher_login_check(username,password)
                    if teacher:
                        st.session_state.is_logged_in = True
                        st.session_state['login_type'] = "teacher"
                        st.session_state.teacher_data = teacher
                        st.toast(f"Welcome back, {teacher['name']}!")
                        st.rerun()
                    else:
                        st.error("Incorrect password. Please try again.")
                else:
                    st.error("Username not found. Please check your username or create a new account.")
            else:
                st.error("Please enter both username and password.")

        if switch_register:
            st.session_state.teacher_auth_mode = "register"
            st.rerun()

    else:
        with st.form("teacher_register_form", clear_on_submit=False):
            st.markdown(dedent("""
            <div style="display: flex; justify-content: center; margin-bottom: 16px;">
                <div style="background: rgba(245,158,11,0.15); width: 64px; height: 64px; border-radius: 18px; display: flex; align-items: center; justify-content: center; font-size: 28px; box-shadow: 0 4px 12px rgba(245,158,11,0.1);">
                    👩‍🏫
                </div>
            </div>
            <div class="form-title">Teacher Portal</div>
            <div class="form-subtitle">Create your account to access the dashboard.</div>
            """), unsafe_allow_html=True)

            st.markdown('<div class="input-label">Username</div>', unsafe_allow_html=True)
            username = st.text_input(
                "Username",
                placeholder="@username",
                label_visibility="collapsed",
                key="reg_username"
            )

            st.markdown('<div class="input-label">Full name</div>', unsafe_allow_html=True)
            name = st.text_input(
                "Full name",
                placeholder="Your full name",
                label_visibility="collapsed",
                key="reg_name"
            )

            st.markdown('<div class="input-label">Password</div>', unsafe_allow_html=True)
            password = st.text_input(
                "Password",
                placeholder="Create password",
                type="password",
                label_visibility="collapsed",
                key="reg_password"
            )

            st.markdown('<div class="input-label">Confirm password</div>', unsafe_allow_html=True)
            confirm_password = st.text_input(
                "Confirm password",
                placeholder="Confirm password",
                type="password",
                label_visibility="collapsed",
                key="reg_confirm_password"
            )

            st.write("")

            btn_col1, btn_col2 = st.columns(2, gap="small")

            with btn_col1:
                register_btn = st.form_submit_button("Register Now", use_container_width=True)

            with btn_col2:
                switch_login = st.form_submit_button("Already registered?", use_container_width=True)

        if register_btn:
            if not username or not name or not password or not confirm_password:
                st.error("Please fill in all fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success ,message = register_teacher(username, password, name)
                st.success("Teacher Registered Successfully! 🎉 Redirecting to Login...")
                st.session_state.teacher_auth_mode = "login"
                st.rerun()

        if switch_login:
            st.session_state.teacher_auth_mode = "login"
            st.rerun()
