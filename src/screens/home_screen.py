import streamlit as st
from src.components.header import global_header

def home_screen():
    global_header(show_auth=False, portal_type="Attendance Portal", show_home=False)

    st.markdown(
        '''
        <div style="text-align: center; padding: 40px 20px 24px; max-width: 600px; margin: 0 auto;">
            <p style="font-size: 12px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #4F6EF7; margin-bottom: 12px;">Choose Your Portal</p>
            <h1 style="font-size: 42px; font-weight: 900; color: #0F172A; letter-spacing: -1px; margin-bottom: 16px; line-height: 1.15;">Welcome Back &#128075;</h1>
            <p style="color: #64748B; font-size: 16px; line-height: 1.6; margin: 0;">Select your portal to manage attendance, track your academic records, and generate live analytics instantly.</p>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.markdown("### 🎓 Student Portal")
            st.write("Mark attendance via facial recognition scan and track your academic records instantly.")
            if st.button("Enter Student Portal →", key="student_btn", use_container_width=True, type="primary"):
                st.session_state["login_type"] = "student"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 👨‍🏫 Teacher Portal")
            st.write("Manage attendance, track student engagement and generate live analytics.")
            if st.button("Enter Teacher Portal →", key="teacher_btn", use_container_width=True, type="primary"):
                st.session_state["login_type"] = "teacher_login"
                st.rerun()

if __name__ == "__main__":
    home_screen()
