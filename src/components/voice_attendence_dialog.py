import streamlit as st
from src.pipelines.voice_pipeline import process_voice_input
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.components.attendence_result_dialog import attendence_result_dialog

@st.dialog('Voice Attendence')
def voice_attendence_dialog(subject_id):
    st.write("Record audio of students saying I am present. Then AI will recognize the students")

    audio_data = None
    audio_data = st.audio_input("Record classroom audio")
    if st.button("Analyze Audio"):
        with st.spinner("Processing Audio data"):
            enrolled_res =  supabase.table('subject_students').select('*,students(*)').eq('subject_id',subject_id).execute()
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No student Enrolled in this course")
                return
            candidate_dict = {
                s['students']['student_id'] : s['students']['voice_embedding']
                for s in enrolled_students if s['students'].get('voice_embedding')
            }

            if not candidate_dict:
                st.error("No enrolled students have voice profiles registered")
                return
            audio_bytes = audio_data.read()

            detected_scores = process_voice_input(audio_bytes,candidate_dict)
            results ,attendence_to_log = [] ,[]
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")  

            for node in enrolled_students:
                student = node['students']
                score = detected_scores.get(student['student_id'],0.0)
                is_present = bool(score>0)
                results.append({
                    "Name" : student['name'],
                    "ID" : student['student_id'],
                    "Source" : score if is_present else "-",
                    "Status" : "️✅Present" if is_present else "❎Absent"
                })

                attendence_to_log.append({
                    'student_id' : student['student_id'],
                    'subject_id' : subject_id,
                    'timestamp' : current_timestamp,
                    'is_present' : bool(is_present)
                })
            st.session_state.voice_attendence_results = (pd.DataFrame(results),attendence_to_log)
    if st.session_state.get("voice_attendence_results"):
        st.divider()

        df_results , logs = st.session_state.voice_attendence_results
        attendence_result_dialog(df_results, logs)
