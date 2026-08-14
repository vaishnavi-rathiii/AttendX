from src.database.config import supabase
import bcrypt


# ----------------------------------------
# Password Hashing
# ----------------------------------------

def hash_pass(pwd):

    # Hash the password using bcrypt
    return bcrypt.hashpw(
        pwd.encode(),
        bcrypt.gensalt()
    ).decode()


def check_pass(pwd, hashed):

    # Check whether the entered password matches the stored hash
    return bcrypt.checkpw(
        pwd.encode(),
        hashed.encode()
    )


# ----------------------------------------
# Check Teacher Exists
# ----------------------------------------

def check_teacher_exists(username):

    # Check for unique usernames
    try:

        response = (
            supabase
            .table("teachers")
            .select("username")
            .eq("username", username)
            .execute()
        )

        return len(response.data) > 0

    except Exception as e:

        # Display database error
        print(f"Error checking teacher: {e}")
        return False


# ----------------------------------------
# Create Teacher
# ----------------------------------------

def create_teacher(username, password, name):

    # Prepare teacher data for insertion
    data = {
        "username": username,
        "password_hash": hash_pass(password),
        "name": name
    }

    # Insert teacher into the database
    try:

        response = (
            supabase
            .table("teachers")
            .insert(data)
            .execute()
        )

        return response.data

    except Exception as e:

        # Display database error
        print(f"Error creating teacher: {e}")
        return []


# ----------------------------------------
# Teacher Login
# ----------------------------------------

def teacher_login(username, password):

    # Find the teacher using the entered username
    try:

        response = (
            supabase
            .table("teachers")
            .select("*")
            .eq("username", username)
            .execute()
        )

    except Exception as e:

        # Display database error
        print(f"Error during teacher login: {e}")
        return None

    # Check whether the teacher exists
    if response.data:

        teacher = response.data[0]

        # Verify the entered password
        try:

            if check_pass(
                password,
                teacher["password_hash"]
            ):
                return teacher

        except Exception as e:

            # Display password verification error
            print(f"Error checking teacher password: {e}")
            return None

    # Return None when login credentials are invalid
    return None


# ----------------------------------------
# Get All Students
# ----------------------------------------

def get_all_students():

    # Fetch all students from the database
    try:

        response = (
            supabase
            .table("students")
            .select("*")
            .execute()
        )

        return response.data

    except Exception as e:

        # Display database error
        print(f"Error getting students: {e}")
        return []


# ----------------------------------------
# Create Student
# ----------------------------------------

def create_student(
    new_name,
    face_embedding=None,
    voice_embedding=None
):

    # Prepare student data
    data = {
        "name": new_name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding
    }

    # Insert student into the database
    try:

        response = (
            supabase
            .table("students")
            .insert(data)
            .execute()
        )

        return response.data

    except Exception as e:

        # Display database error
        print(f"Error creating student: {e}")
        return []


# ----------------------------------------
# Create Subject
# ----------------------------------------

def create_subject(
    subject_code,
    name,
    section,
    teacher_id
):

    # Prepare subject data
    data = {
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id
    }

    # Insert subject into the database
    try:

        response = (
            supabase
            .table("subjects")
            .insert(data)
            .execute()
        )

        return response.data

    except Exception as e:

        # Display database error
        print(f"Error creating subject: {e}")
        return []


# ----------------------------------------
# Get Teacher Subjects
# ----------------------------------------

def get_teacher_subjects(teacher_id):

    # Get all subjects created by the teacher
    try:

        response = (
            supabase
            .table('subjects')
            .select(
                "*, subject_students(count), "
                "attendance_logs(timestamp)"
            )
            .eq("teacher_id", teacher_id)
            .execute()
        )

        subjects = response.data

    except Exception as e:

        # Display database error
        print(f"Error getting teacher subjects: {e}")
        return []

    # ----------------------------------------
    # Calculate Subject Statistics
    # ----------------------------------------

    for sub in subjects:

        # Calculate total enrolled students
        sub['total_students'] = (
            sub.get("subject_students", [{}])[0].get(
                'count',
                0
            )
            if sub.get('subject_students')
            else 0
        )

        # Get attendance records
        attendance = sub.get('attendance_logs', [])

        # Count unique attendance sessions
        unique_sessions = len(
            set(
                log['timestamp']
                for log in attendance
            )
        )

        sub['total_classes'] = unique_sessions

        # Remove unnecessary fields
        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects


# ----------------------------------------
# Enroll Student to Subject
# ----------------------------------------

def enroll_student_to_subject(
    student_id,
    subject_id
):

    # Prepare enrollment data
    data = {
        'student_id': student_id,
        "subject_id": subject_id
    }

    # Add student to the subject
    try:

        response = (
            supabase
            .table('subject_students')
            .insert(data)
            .execute()
        )

        return response.data

    except Exception as e:

        # Display database error
        print(f"Error enrolling student: {e}")
        return []


# ----------------------------------------
# Unenroll Student from Subject
# ----------------------------------------

def unenroll_student_to_subject(
    student_id,
    subject_id
):

    # Remove student from the subject
    try:

        response = (
            supabase
            .table('subject_students')
            .delete()
            .eq('student_id', student_id)
            .eq('subject_id', subject_id)
            .execute()
        )

        return response.data

    except Exception as e:

        # Display database error
        print(f"Error unenrolling student: {e}")
        return []


# ----------------------------------------
# Get Student Subjects
# ----------------------------------------

def get_student_subjects(student_id):

    # Get subjects in which the student is enrolled
    try:

        response = (
            supabase
            .table('subject_students')
            .select('*, subjects(*)')
            .eq('student_id', student_id)
            .execute()
        )

        return response.data

    except Exception as e:

        # Display database error
        print(f"Error getting student subjects: {e}")
        return []


# ----------------------------------------
# Get Student Attendance
# ----------------------------------------

def get_student_attendance(student_id):

    # Get attendance records for the student
    try:

        response = (
            supabase
            .table('attendance_logs')
            .select('*, subjects(*)')
            .eq('student_id', student_id)
            .execute()
        )

        return response.data

    except Exception as e:

        # Display database error
        print(f"Error getting student attendance: {e}")
        return []


# ----------------------------------------
# Create Attendance
# ----------------------------------------

def create_attendance(logs):

    # Insert attendance records into the database
    try:

        response = (
            supabase
            .table('attendance_logs')
            .insert(logs)
            .execute()
        )

        return response.data

    except Exception as e:

        # Display database error
        print(f"Error creating attendance: {e}")
        return []


# ----------------------------------------
# Get Attendance for Teacher
# ----------------------------------------

def get_attendance_for_teacher(teacher_id):

    # Get attendance records for subjects belonging to the teacher
    try:

        response = (
            supabase
            .table('attendance_logs')
            .select(
                "*, subjects!inner(*)"
            )
            .eq(
                'subjects.teacher_id',
                teacher_id
            )
            .execute()
        )

        return response.data

    except Exception as e:

        # Display database error
        print(f"Error getting teacher attendance: {e}")
        return []