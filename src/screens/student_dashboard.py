import time
from textwrap import dedent

import streamlit as st
from src.components.subject_card import subject_card
import numpy as np
from PIL import Image
from src.pipelines.face_pipeline import predict_face , extract_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students , create_student , unenroll_student_to_subject , get_student_subjects ,get_student_attendence
from src.components.enroll_dialog import enroll_dialog


from src.components.header import global_header

def student_ui():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    
    global_header(show_auth=True, user_name=student_data['name'], portal_type="Student Portal")
    
    st.markdown(f"""
        <div style="margin-bottom: 32px;">
            <h1 style="color: #f8fafc; font-size: 32px; margin-bottom: 4px; font-weight: 800; letter-spacing: -0.5px;">Welcome back, {student_data['name']} 👋</h1>
            <p style="color: #38bdf8; font-size: 15px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Track your attendance</p>
        </div>
    """, unsafe_allow_html=True)

    c1 , c2 = st.columns(2)
    with c1:
        st.header("your Enrolled Subjects")
    with c2:
        if st.button('Enroll in Subject',type="primary",width="stretch"):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading Your Enrolled Subjects...'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendence(student_id)

    stats_map = {}

    for log in logs:
        sid = log.get('subject_id')
        if not sid:
            continue

        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}

        stats_map[sid]['total'] += 1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1
    
    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node.get('subjects', {})
        if not sub:
            continue
        sid = sub.get('subject_id')

        stats = stats_map.get(sid, {"total": 0, "attended": 0})
        
        def make_unenroll_btn(curr_sid, curr_sub_name):
            def btn_callback():
                if st.button("Unenroll from this course", key=f"unenroll_{curr_sid}", type="primary", width="stretch", icon=":material/delete_forever:"):
                    unenroll_student_to_subject(student_id, curr_sid)
                    st.toast(f"Unenrolled from {curr_sub_name} successfully")
                    import time
                    time.sleep(1)
                    st.rerun()
            return btn_callback

        with cols[i % 2]:
            subject_card(
                name=sub.get('name', 'Unknown'),
                code=sub.get("subject_code", ""),
                section=sub.get('section', ""),
                stats=[
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attendance', stats['attended'])
                ],
                footer_callback=make_unenroll_btn(sid, sub.get('name', 'Unknown'))
            )
        

def student_dashboard():

    if "student_data" in st.session_state:
        student_ui()
        return

    global_header(show_auth=False, portal_type="Student Portal", show_home=True)

    st.subheader("Student Login")

    captured_image = st.camera_input("Capture Image for Login . Take a picture")
    show_registration = False

    if captured_image:
        img_array = np.array(Image.open(captured_image))
        with st.spinner("Processing Image..."):
            detected , all_ids , num_faces = predict_face(img_array)

            if num_faces == 0:
                st.warning("No face detected. Please try again.")
            elif num_faces > 1:
                st.warning("Multiple faces detected. Please ensure only one face is in the frame.")
            else:      
                if detected:
                    st.success("Face recognized successfully!")
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome back, {student['name']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.info("Face recognized, but student data not found. Please register or try again.")
                        show_registration = True
                else:
                    st.info("Face not recognized. Please register or try again.")
                    show_registration = True

    if show_registration:
        with st.container(border=True):
            st.header("Student Registration")
            name = st.text_input("Full Name")

            st.subheader("Optional : Voice Enrollment")
            st.info("Enroll your voice only attendence")

            audio_data = None

            try:
                audio_data = st.audio_input("Record your voice, say 'Present' to enroll")
            except Exception as e:
                st.warning("Audio failed to capture. Please ensure you have a microphone and try again.")
            
            if st.button("Create Account",type="primary"):
                if name:
                    with st.spinner("Creating your account..."):
                        img = np.array(Image.open(captured_image))
                        encodings = extract_face_embeddings(img)
                        if encodings:
                            face_embedding = list(encodings[0])  # Assuming one face for registration
                            # Here you would typically save the new student data to the database, including the face embedding and audio data if available
                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())
                            response_data = create_student(name ,face_embedding = face_embedding,  voice_embedding = voice_emb)  

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response_data[0] if isinstance(response_data, list) else response_data
                                st.toast(f"Profile created successfully, {name}!")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Failed to extract face. Please try again.")
                else:
                    st.warning("Please enter your name to register.")

