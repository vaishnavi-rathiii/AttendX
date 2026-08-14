import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


# ----------------------------------------
# Load Dlib Face Recognition Models
# ----------------------------------------

@st.cache_resource
def load_dlib_models():

    try:

        # Load frontal face detector
        detector = dlib.get_frontal_face_detector()

        # Load facial landmark predictor
        shapePredictor = dlib.shape_predictor(
            face_recognition_models.pose_predictor_model_location()
        )

        # Load face recognition model
        faceRecognition = dlib.face_recognition_model_v1(
            face_recognition_models.face_recognition_model_location()
        )

        return detector, shapePredictor, faceRecognition

    except Exception as e:

        # Handle dlib model loading errors
        st.error(f"Unable to load face recognition models: {e}")
        return None, None, None


# ----------------------------------------
# Get Face Embeddings
# ----------------------------------------

def get_face_embeddings(image_np):

    # Load dlib models
    detector, shapePredictor, faceRecognition = load_dlib_models()

    # Check whether models loaded successfully
    if not detector or not shapePredictor or not faceRecognition:
        return []

    try:

        # Detect faces in the image
        faces = detector(image_np, 1)

        encodings = []

        # ----------------------------------------
        # Generate Embeddings for Each Face
        # ----------------------------------------

        for face in faces:

            # Detect facial landmarks
            shape = shapePredictor(image_np, face)

            # Generate 128-dimensional face descriptor
            face_descriptor = faceRecognition.compute_face_descriptor(
                image_np,
                shape,
                1
            )

            # Convert descriptor to NumPy array
            encodings.append(
                np.array(face_descriptor)
            )

        return encodings

    except Exception as e:

        # Handle face detection/embedding errors
        st.error(f"Unable to generate face embeddings: {e}")
        return []


# ----------------------------------------
# Train Face Recognition Model
# ----------------------------------------

@st.cache_resource
def get_trained_model():

    X = []
    y = []

    # ----------------------------------------
    # Get Students from Database
    # ----------------------------------------

    try:

        student_db = get_all_students()

    except Exception as e:

        # Handle database errors
        st.error(f"Unable to load students: {e}")
        return None

    if not student_db:
        return None

    # ----------------------------------------
    # Collect Face Embeddings and Student IDs
    # ----------------------------------------

    for student in student_db:

        embedding = student.get("face_embedding")
        student_id = student.get("student_id")

        if embedding and student_id is not None:

            try:

                # Convert embedding to NumPy array
                embedding = np.array(
                    embedding,
                    dtype=float
                )

                # Make sure the embedding has the expected size
                if embedding.shape == (128,):

                    X.append(embedding)
                    y.append(student_id)

            except Exception as e:

                # Skip invalid face embeddings
                print(
                    f"Invalid face embedding skipped: {e}"
                )
                continue

    # ----------------------------------------
    # Check Valid Face Embeddings
    # ----------------------------------------

    if len(X) == 0:
        return None

    # ----------------------------------------
    # Get Unique Students / Classes
    # ----------------------------------------

    unique_students = list(set(y))

    # ----------------------------------------
    # One Student Case
    # ----------------------------------------

    # SVC cannot train with only one class.
    # Therefore, don't create an SVC in this case.

    if len(unique_students) == 1:

        return {
            "classifier": None,
            "X_train": X,
            "y_train": y
        }

    # ----------------------------------------
    # Multiple Students Case
    # ----------------------------------------

    classifier = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    # ----------------------------------------
    # Train SVC Classifier
    # ----------------------------------------

    try:

        classifier.fit(X, y)

    except ValueError as e:

        # Handle model training errors
        st.error(f"Model training failed: {e}")
        return None

    except Exception as e:

        # Handle unexpected training errors
        st.error(f"Unexpected model training error: {e}")
        return None

    return {
        "classifier": classifier,
        "X_train": X,
        "y_train": y
    }


# ----------------------------------------
# Train / Refresh Classifier
# ----------------------------------------

def train_classifier():

    # Clear cached model so it gets trained again
    get_trained_model.clear()

    # Train the classifier again
    model_data = get_trained_model()

    return bool(model_data)


# ----------------------------------------
# Predict Attendance
# ----------------------------------------

def predict_attendance(class_image_np):

    # ----------------------------------------
    # Detect Faces
    # ----------------------------------------

    try:

        encodings = get_face_embeddings(
            class_image_np
        )

    except Exception as e:

        # Handle face detection errors
        st.error(f"Unable to process classroom image: {e}")
        return {}, [], 0

    detected_student = {}

    # ----------------------------------------
    # Load Trained Model
    # ----------------------------------------

    try:

        model_data = get_trained_model()

    except Exception as e:

        # Handle model loading errors
        st.error(f"Unable to load trained model: {e}")
        return detected_student, [], len(encodings)

    if not model_data:

        return detected_student, [], len(encodings)

    classifier = model_data["classifier"]
    X_train = model_data["X_train"]
    y_train = model_data["y_train"]

    # ----------------------------------------
    # Get Unique Student IDs
    # ----------------------------------------

    all_students = sorted(
        list(set(y_train))
    )

    # ----------------------------------------
    # No Students Case
    # ----------------------------------------

    if len(all_students) == 0:

        return detected_student, [], len(encodings)

    # ----------------------------------------
    # Process Each Detected Face
    # ----------------------------------------

    for encoding in encodings:

        # ----------------------------------------
        # Multiple Students
        # ----------------------------------------

        if len(all_students) >= 2:

            try:

                predicted_id = classifier.predict(
                    [encoding]
                )[0]

                predicted_id = int(predicted_id)

            except Exception as e:

                # Handle prediction errors
                st.error(
                    f"Face prediction failed: {e}"
                )
                continue

        # ----------------------------------------
        # One Student
        # ----------------------------------------

        else:

            predicted_id = int(
                all_students[0]
            )

        # ----------------------------------------
        # Find Embeddings Belonging to Predicted Student
        # ----------------------------------------

        student_embeddings = []

        for index, student_id in enumerate(y_train):

            if student_id == predicted_id:

                student_embeddings.append(
                    X_train[index]
                )

        # Student has no valid embedding
        if not student_embeddings:
            continue

        # ----------------------------------------
        # Find Closest Embedding
        # ----------------------------------------

        distances = []

        for student_embedding in student_embeddings:

            distance = np.linalg.norm(
                student_embedding - encoding
            )

            distances.append(distance)

        best_match_score = min(distances)

        # ----------------------------------------
        # Face Match Threshold
        # ----------------------------------------

        resemblance_threshold = 0.6

        if best_match_score <= resemblance_threshold:

            detected_student[predicted_id] = True

    # ----------------------------------------
    # Return Attendance Results
    # ----------------------------------------

    return (
        detected_student,
        all_students,
        len(encodings)
    )