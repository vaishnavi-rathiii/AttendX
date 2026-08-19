# AttendX

> **AI-Powered Attendance Management System**

AttendX is a smart attendance management system designed to make attendance faster, simpler, and more reliable using **Artificial Intelligence**.

The system combines **Face Recognition** and **Voice Recognition** to identify students and record attendance, while providing separate workflows for teachers and students.



## 🌐 Live Demo

Try AttendX here:

**https://attendx-ai.streamlit.app/**

> The live deployment may be updated as new features and improvements are added.

---

## ✨ Features

- 👤 **Student Face Recognition**
  - Captures a student's face through the camera.
  - Generates facial embeddings.
  - Recognizes registered students during attendance.

- 🎙️ **Voice Recognition**
  - Supports optional voice enrollment.
  - Generates speaker embeddings for voice-based identification.

- 👨‍🏫 **Teacher Authentication**
  - Teacher registration and login.
  - Passwords are securely hashed using bcrypt.

- 👨‍🎓 **Student Registration**
  - Register a new student after face recognition fails to identify them.
  - Store face and optional voice embeddings.

- 📊 **Attendance Management**
  - Uses recognized student identities for attendance-related operations.
  - Student and teacher data are stored in Supabase.

- 🗄️ **Supabase Database**
  - Stores users, embeddings, subjects, and attendance-related data.

- 🎨 **Streamlit Interface**
  - Clean and responsive web interface.
  - Custom styling and dashboard components.

---

## 🧠 How AttendX Works

```text
                    ┌───────────────────┐
                    │      AttendX      │
                    └─────────┬─────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
          👨‍🏫 Teacher Flow           👨‍🎓 Student Flow
                 │                         │
          Login / Register          FaceID Login
                 │                         │
        Manage Attendance          Face Detection
        & Subjects                      │
                                  ┌───────┴───────┐
                                  │               │
                              Recognized       Not Found
                                  │               │
                              Login /       New Student
                              Attendance     Registration
                                                  │
                                         Face + Optional Voice
                                                  │
                                              Supabase
```

---

## 🔬 AI Pipeline

### Face Recognition

AttendX uses a dlib-based face recognition pipeline:

```text
Camera Image
     ↓
Face Detection
     ↓
Facial Landmark Detection
     ↓
Face Embedding Generation
     ↓
SVM Classification
     ↓
Similarity / Threshold Check
     ↓
Student Identification
```

The system generates a numerical representation of the detected face and compares it against registered student embeddings.

### Voice Recognition

The voice pipeline uses **Resemblyzer** to generate speaker embeddings:

```text
Audio Input
    ↓
Audio Preprocessing
    ↓
Voice Embedding
    ↓
Speaker Representation
    ↓
Voice-based Identification
```

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Frontend / UI | Streamlit |
| Programming Language | Python |
| Database | Supabase |
| Face Detection & Recognition | dlib, face_recognition_models |
| Machine Learning | Scikit-learn |
| Face Classifier | SVM |
| Voice Recognition | Resemblyzer |
| Audio Processing | Librosa, SoundFile |
| Deep Learning | PyTorch, TorchAudio |
| Image Processing | Pillow, NumPy |
| Authentication | bcrypt |
| QR Generation | Segno |

---

## 📁 Project Structure

```text
AttendX/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── components/
│   │   ├── header.py
│   │   ├── footer.py
│   │   ├── dialog_create_subject.py
│   │   └── dialog_voice_attendance.py
│   │
│   ├── database/
│   │   ├── config.py
│   │   └── db.py
│   │
│   ├── pipelines/
│   │   ├── face_pipeline.py
│   │   └── voice_pipeline.py
│   │
│   ├── screens/
│   │   ├── teacher_screen.py
│   │   └── student_screen.py
│   │
│   └── ui/
│       └── base_layout.py
│
└── .streamlit/
    └── secrets.toml
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AttendX.git
cd AttendX
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Supabase

Create a Supabase project and configure the required database tables.

For local development, create:

```text
.streamlit/secrets.toml
```

Add:

```toml
SUPABASE_URL = "your-supabase-project-url"
SUPABASE_KEY = "your-supabase-anon-key"
```

**Never commit `secrets.toml` or expose your Supabase credentials publicly.**

### 6. Run AttendX

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

## ☁️ Deployment

AttendX can be deployed using **Streamlit Community Cloud**.

General deployment steps:

1. Push the project to GitHub.
2. Connect the repository to Streamlit Community Cloud.
3. Select `app.py` as the main application file.
4. Add the Supabase credentials under the app's **Secrets**.
5. Deploy the application.

---

## 🔐 Security

AttendX follows several basic security practices:

- Teacher passwords are hashed using **bcrypt**.
- Supabase credentials are stored using Streamlit secrets.
- Sensitive credentials should never be committed to GitHub.
- Face and voice data are represented as embeddings rather than relying on plain image/audio storage for recognition.

> **Important:** For production deployment, biometric data requires appropriate privacy, consent, access-control, retention, and security policies.

---

## 🎯 Use Case

AttendX is designed for educational environments where teachers need a faster way to manage attendance.

### Example workflow

```text
Teacher
   ↓
Logs into AttendX
   ↓
Student opens FaceID attendance
   ↓
Camera captures face
   ↓
AI identifies student
   ↓
Attendance workflow
   ↓
Record stored in database
```

For a new student:

```text
Face not recognized
        ↓
Student registration
        ↓
Enter name
        ↓
Capture face embedding
        ↓
Optional voice enrollment
        ↓
Save profile
        ↓
Student becomes available for recognition
```

---

## 🌱 Future Improvements

Potential future improvements include:

- 📱 Mobile-friendly interface
- 📈 Attendance analytics and visual reports
- 📅 Automatic attendance summaries
- 📧 Attendance notifications
- 🔒 Stronger biometric security and access controls
- 🧑‍🏫 Advanced teacher dashboard
- 📥 CSV / Excel attendance export
- 🏫 Multi-class and multi-subject management
- ☁️ Improved cloud deployment and scaling

---

## 📌 Project Status

**AttendX is an actively developed AI-based attendance project.**

Features and implementation may continue to evolve as the project progresses.

---

## 👩‍💻 Author

**Vaishnavi Rathi**

Diploma in Artificial Intelligence & Machine Learning

---

## 📄 License

**Copyright © 2026 Vaishnavi Rathi. All Rights Reserved.**

This repository and its source code are provided for **educational and portfolio viewing purposes only**.

### Restrictions

- ❌ No copying or redistributing the source code
- ❌ No claiming this project or its source code as your own
- ❌ No publishing modified or unmodified copies of this repository
- ❌ No commercial use without explicit written permission
- ❌ No reusing substantial portions of the source code in another project without permission

Viewing and studying the repository does **not** grant permission to reproduce, redistribute, modify, or commercially use the source code.

For permission to use any part of AttendX beyond personal educational viewing, contact the author.

---

## 👩‍💻 Author

**Vaishnavi Rathi**

Diploma in Artificial Intelligence & Machine Learning

---

⭐ If you find AttendX interesting, consider starring the repository.
