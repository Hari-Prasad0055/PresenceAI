from src.database.db import get_teacher_subjects
import sys
import json

try:
    subjects = get_teacher_subjects("some_teacher_id")
    print("Success")
except Exception as e:
    print("Error:", e)
