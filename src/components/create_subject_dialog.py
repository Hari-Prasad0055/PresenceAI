import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter subject details")
    sub_id = st.text_input("Subject Code",placeholder="e.g. CS101")
    sub_name = st.text_input("Subject Name",placeholder="e.g. Introduction to Python")
    sub_section = st.text_input("Section",placeholder="e.g. A")
    if st.button("Create Subject",type="primary",width="stretch"):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(teacher_id, sub_id, sub_name, sub_section)
                st.toast("Subject created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to create subject: {str(e)}")
    else:
        st.warning("Please fill in all fields to create a subject.")  
        