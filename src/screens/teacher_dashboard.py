import streamlit as st
import numpy as np
import pandas as pd
from textwrap import dedent
from datetime import datetime
from src.database.config import supabase
from src.components.voice_attendence_dialog import voice_attendence_dialog
from src.components.create_subject_dialog import create_subject_dialog
from src.database.db import get_teacher_subjects,get_attendence_for_teacher
from src.components.subject_card import subject_card
from src.components.share_subject_dialog import share_subject_dialog
from src.components.add_photos_dialog import add_photos_dialog
from src.components.attendence_result_dialog import show_attendece_result
from src.pipelines.face_pipeline import predict_face
from src.components.header import global_header

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    
    global_header(show_auth=True, user_name=teacher_data['name'], portal_type="Teacher Portal")
    
    st.markdown(f"""
        <div style="margin-bottom: 32px;">
            <h1 class="welcome-heading">Welcome back, {teacher_data['name']} 👋</h1>
            <p class="welcome-subheading">MANAGE YOUR CLASSES</p>
        </div>
    """, unsafe_allow_html=True)

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    # Navigation Tabs
    tab1, tab2 , tab3 = st.columns(3)
    with tab1 :
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "secondary"
        if st.button('Take Attendance' ,type=type1, use_container_width=True, icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()
    with tab2 :
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "secondary"
        if st.button('Manage Subjects' ,type=type2, use_container_width=True, icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()
    with tab3 :
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "secondary"
        if st.button('Attendance Records' ,type=type3, use_container_width=True, icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.markdown("<hr style='border: none; height: 1px; background-color: #e2e8f0; margin: 24px 0;' />", unsafe_allow_html=True)

    # Content Area
    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.markdown('<h2 class="attendance-heading">Take AI Attendance</h2>', unsafe_allow_html=True)

    if 'attendence_images' not in st.session_state:
        st.session_state.attendence_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning("you haven't created any subjects yet!")
        return
    subject_options = {f'{s['name']} - {s['subject_code']}': s['subject_id'] for s in subjects}

    col1 , col2 = st.columns([3,1],vertical_alignment="bottom")

    with col1:
        selected_subject_label = st.selectbox('select subject',options=list(subject_options.keys()))
    with col2:
        if st.button('Add photos',type="primary"):
            add_photos_dialog()
    
    selected_subject_id = subject_options[selected_subject_label]
    st.divider()

    if st.session_state.attendence_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx , img in enumerate(st.session_state.attendence_images):
            with gallery_cols[idx % 4]:
                st.image(img,width="stretch",caption=f"photo {idx+1}")
    
    has_photos = bool(st.session_state.attendence_images)
    c1 , c2 , c3 = st.columns(3)
    with c1:
        if st.button("Clear All photos", width="stretch",type="tertiary",icon=":material/delete:",disabled=not has_photos):
            st.session_state.attendence_images = []
            st.rerun()
    with c2:
        if st.button("Run Face Analysis", width="stretch",type="tertiary",icon=":material/analytics:",disabled=not has_photos):
            with st.spinner("Deep Scanning classroom photos..."):
                all_detected_ids = {}

                for idx , img in enumerate(st.session_state.attendence_images):
                    img_np = np.array(img.convert('RGB'))

                    detected , _ , _ = predict_face(img_np)
                    
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id,[]).append(f"photo {idx+1}")
                enrolled_res =  supabase.table('subject_students').select('*,students(*)').eq('subject_id',selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning("No student Enrolled in this course")
                else:

                    results ,attendence_to_log = [] ,[]
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")  

                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']),[])
                        is_present = len(sources) >0
                        results.append({
                            "Name" : student['name'],
                            "ID" : student['student_id'],
                            "Source" : ",".join(sources) if is_present else "-",
                            "Status" : "️✅Present" if is_present else "❎Absent"
                        })

                        attendence_to_log.append({
                            'student_id' : student['student_id'],
                            'subject_id' : selected_subject_id,
                            'timestamp' : current_timestamp,
                            'is_present' : bool(is_present)
                        })
                show_attendece_result(pd.DataFrame(results),attendence_to_log)
    with c3:
        if st.button("Use Voice Attendence",type="primary",width="stretch",icon=":material/mic:"):
            voice_attendence_dialog(selected_subject_id)



                   

def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    
    # Header for Manage Subjects
    c1, c2 = st.columns([3, 1], vertical_alignment="center")
    with c1:
        st.markdown('<h2 class="attendance-heading" style="font-size: 24px !important;">Manage Subjects</h2>', unsafe_allow_html=True)
        st.markdown('<p style="margin-top: -5px; margin-bottom: 20px;">View and manage your current classes.</p>', unsafe_allow_html=True)

    with c2:
        if st.button("Add Subject", type="primary", use_container_width=True, icon=":material/add:"):
            create_subject_dialog(teacher_id)

    # List all the subjects of the teacher here
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        # Create a 2-column grid
        cols = st.columns(2, gap="large")
        
        for index, subject in enumerate(subjects):
            with cols[index % 2]:
                stats = [
                    ("👨‍👦‍👦", "Total Students", subject.get("total_students", 0)),
                    ("⏰","Classes Taken", subject.get("total_classes", 0))
                ]

                def make_share_btn(subj):
                    def share_btn():
                        if st.button(f"Share Code: {subj['name']}", key=f"share_{subj['subject_code']}", icon=":material/share:"):
                            share_subject_dialog(subj['name'], subj['subject_code'])
                    return share_btn

                subject_card(
                    name=subject['name'],
                    code=subject['subject_code'],
                    section=subject['section'],
                    stats=stats,
                    footer_callback=make_share_btn(subject)
                )
                st.write("")
    else:
        st.info("No subjects found. Please add a subject to get started.")


def teacher_tab_attendance_records():
    st.markdown('<h2 class="attendance-heading">Attendance Records</h2>', unsafe_allow_html=True)

    teacher_id = st.session_state.teacher_data["teacher_id"]

    records = get_attendence_for_teacher(teacher_id)
    if not records:
        return
    
    data =[]

    for r in records:
        ts = r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "subject": r['subjects']['name'],
            "subject_code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = df.groupby(["ts_group","Time","subject","subject_code"]).agg(
        Present_count = ('is_present','sum'),
        Total_count = ('is_present','count')
    ).reset_index()

    summary["Attendence Stats"] = (
        "✅ " + summary['Present_count'].astype(str) + " / " +
        summary['Total_count'].astype(str) + " students"
    )

    display_df = summary.sort_values(by='ts_group', ascending=False)[['Time','subject','subject_code','Attendence Stats']]
    
    st.dataframe(display_df, width="stretch", hide_index=True)