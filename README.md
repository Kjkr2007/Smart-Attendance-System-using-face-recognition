# Smart-Attendance-System-using-face-recognition
A modern AI-powered attendance system that uses face recognition to automatically mark student attendance in real-time. This project combines a sleek web interface with a powerful backend to create a complete, production-ready solution.
🚀 Features
📷 Real-time Face Recognition
Detects and identifies students using webcam
Automatically marks attendance
➕ Student Registration
Register students using live camera or image upload
Stores facial encodings for future recognition
📊 Attendance Management
Prevents duplicate entries for the same day
Maintains structured attendance records
📥 Excel Export
Download attendance data in .xlsx format
Automatically updates records
👥 Student Management
View all registered students
Remove students from the system
📋 Live Dashboard
Real-time scan feed
Attendance stats (Total, Registered, Scans)
🧠 Tech Stack

Frontend

HTML5, CSS3, JavaScript (Custom UI)

Backend

Flask

AI / Computer Vision

face_recognition
OpenCV

Data Handling

Pandas
Excel (.xlsx) for storage
📁 Project Structure
attendance-system/
│
├── app.py
├── students/
├── encodings.pkl
├── attendance.xlsx
├── templates/
│   └── index.html
⚙️ Installation
pip install flask face_recognition opencv-python pandas openpyxl numpy
▶️ Run the Project
python app.py

Open browser:

http://127.0.0.1:5000
📊 Attendance Format
Name	Date	Time	Status
Arjun	03-05-2026	10:32:12	Present
☁️ Deployment

This project can be deployed using:

Render
Railway
Amazon Web Services
⚠️ Notes
Works best with clear, front-facing images
Camera access must be enabled in browser
First-time setup may take time due to model loading
💡 Future Improvements
Mobile app integration
Cloud database (MongoDB / Firebase)
Face anti-spoofing detection
Multi-class attendance tracking
Admin authentication system
👨‍💻 Author

K Jaswanth Kumar Reddy
Aspiring Cloud Architect | CSE (Cloud Computing)
