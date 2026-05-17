import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def extract_face_embeddings(image_np):
    detector , sp , facerec = load_dlib_models()
    faces = detector(image_np,1)

    embeddings =[]
    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape,1) #128 embeddings
        embeddings.append(np.array(face_descriptor))

    return embeddings


@st.cache_resource
def train_model():
    X =[]
    y =[]

    students = get_all_students()

    if not students:
        return None
    for student in students:
        embedding = student.get("face_embedding")
        if embedding:
            X.append(embedding)
            y.append(student.get("student_id"))

    if len(X) == 0:
        return None
    
    clf = SVC(kernel="linear", probability=True,class_weight="balanced")

    try:
        clf.fit(X,y)
    except Exception as e:
        pass
    return {"clf": clf, "X": X, "y": y}

def train_classifier():
    st.cache_resource.clear()
    model_data = train_model()
    return bool(model_data)

def predict_face(class_image_np):
    encodings = extract_face_embeddings(class_image_np)

    detected_student = {}

    model_data = train_model()
    if not model_data:
        return detected_student,[],len(encodings)
    
    clf,X_train,y_train = model_data["clf"], model_data["X"], model_data["y"]

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        if len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        student_emnbedding = X_train[y_train.index(predicted_id)]

        best_match_score = np.linalg.norm(np.array(student_emnbedding) - np.array(encoding))
        if best_match_score < 0.6:
            detected_student[predicted_id] = True

    return detected_student,all_students,len(encodings)
