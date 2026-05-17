from src.database.config import supabase
import bcrypt

def check_teacher_exists(username):
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0


def create_teacher(username, password, name):

    data = {
        "username": username,
        "password": bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        "name":name
    }
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login_check(username,password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if bcrypt.checkpw(password.encode('utf-8'), teacher['password'].encode('utf-8')):
            return teacher
    return None


def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

def create_student(name, face_embedding, voice_embedding=None):
    data = {
        "name": name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding
    }
    response = supabase.table("students").insert(data).execute()
    return response.data


def create_subject(teacher_id, subject_id, subject_name, section):
    data ={
        "teacher_id": teacher_id,
        "subject_code": subject_id,
        "name": subject_name,
        "section": section
    }
    response = supabase.table("subjects").insert(data).execute()
    return response.data


def get_teacher_subjects(teacher_id):
    response = supabase.table("subjects").select("*", "subject_students(count)", "attendence_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data

    for subject in subjects:
        subj_students = subject.get("subject_students")
        if isinstance(subj_students, list) and subj_students:
            subject['total_students'] = subj_students[0].get("count", 0) if isinstance(subj_students[0], dict) else len(subj_students)
        elif isinstance(subj_students, dict):
            subject['total_students'] = subj_students.get("count", 0)
        else:
            subject['total_students'] = 0
        attendence_logs = subject.get("attendence_logs", [])
        unique_sessions = len(set(log['timestamp'] for log in attendence_logs)) if attendence_logs else 0
        subject['total_classes'] = unique_sessions
    
    return subjects

def enroll_student_to_subject(student_id,subject_id):
    data = {
        'student_id' : student_id,
        'subject_id' : subject_id
    }
    response = supabase.table("subject_students").insert(data).execute()
    return response.data

def unenroll_student_to_subject(student_id,subject_id):
    data = {
        'student_id' : student_id,
        'subject_id' : subject_id
    }
    response = supabase.table("subject_students").delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
    return response.data


def get_student_subjects(student_id):
    response = supabase.table("subject_students").select('*,subjects(*)').eq('student_id',student_id).execute()
    return response.data

def get_student_attendence(student_id):
    response = supabase.table("attendence_logs").select('*,subjects(*)').eq('student_id',student_id).execute()
    return response.data

def create_attendence(logs):
    response = supabase.table("attendence_logs").insert(logs).execute()
    return response.data

def get_attendence_for_teacher(teacher_id):
    response = supabase.table("attendence_logs").select("*,subjects!inner(*)").eq('subjects.teacher_id',teacher_id).execute()
    return response.data
