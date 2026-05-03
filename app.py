from flask import Flask, render_template, request, jsonify, send_file
import face_recognition
import numpy as np
import os
import pickle
import base64
import cv2
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# ---------------- FILES ----------------
ENCODINGS_FILE = "encodings.pkl"
STUDENTS_DIR = "students"
ATTENDANCE_FILE = "attendance.xlsx"

if not os.path.exists(STUDENTS_DIR):
    os.makedirs(STUDENTS_DIR)

# ---------------- LOAD ENCODINGS ----------------
def load_encodings():
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, "rb") as f:
            return pickle.load(f)
    return {"encodings": [], "names": []}

def save_encodings(data):
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(data, f)

# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data["name"]
    image_data = data["image"]

    img_bytes = base64.b64decode(image_data.split(",")[1])
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(rgb)

    if not faces:
        return jsonify({"success": False, "message": "No face detected"})

    encoding = face_recognition.face_encodings(rgb, faces)[0]

    data = load_encodings()
    data["encodings"].append(encoding)
    data["names"].append(name)
    save_encodings(data)

    cv2.imwrite(f"{STUDENTS_DIR}/{name}.jpg", img)

    return jsonify({"success": True, "message": f"{name} registered successfully"})

# ---------------- RECOGNIZE ----------------
@app.route("/recognize", methods=["POST"])
def recognize():
    data = request.json
    image_data = data["image"]

    img_bytes = base64.b64decode(image_data.split(",")[1])
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, faces)

    known = load_encodings()

    results = []

    for (top, right, bottom, left), face_enc in zip(faces, encodings):
        matches = face_recognition.compare_faces(known["encodings"], face_enc)
        name = "Unknown"
        confidence = 0

        if True in matches:
            idx = matches.index(True)
            name = known["names"][idx]
            confidence = 0.9

            mark_attendance(name)

        results.append({
            "name": name,
            "confidence": confidence,
            "bbox": [left, top, right-left, bottom-top],
            "marked": name != "Unknown",
            "message": "Attendance Marked" if name != "Unknown" else "Unknown Face"
        })

    return jsonify({"success": True, "results": results})

# ---------------- ATTENDANCE ----------------
def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%H:%M:%S")

    if not os.path.exists(ATTENDANCE_FILE):
        df = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
    else:
        df = pd.read_excel(ATTENDANCE_FILE)

    if ((df["Name"] == name) & (df["Date"] == date)).any():
        return

    new_row = {"Name": name, "Date": date, "Time": time, "Status": "Present"}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(ATTENDANCE_FILE, index=False)

# ---------------- GET RECORDS ----------------
@app.route("/attendance")
def get_attendance():
    if not os.path.exists(ATTENDANCE_FILE):
        return jsonify({"records": []})

    df = pd.read_excel(ATTENDANCE_FILE)
    records = []

    for i, row in df.iterrows():
        records.append({
            "sno": i+1,
            "name": row["Name"],
            "date": row["Date"],
            "time": row["Time"],
            "status": row["Status"]
        })

    return jsonify({"records": records})

# ---------------- STUDENTS ----------------
@app.route("/students")
def students():
    data = load_encodings()
    return jsonify({"students": data["names"]})

# ---------------- DELETE ----------------
@app.route("/delete_student", methods=["POST"])
def delete_student():
    name = request.json["name"]
    data = load_encodings()

    if name in data["names"]:
        idx = data["names"].index(name)
        data["names"].pop(idx)
        data["encodings"].pop(idx)
        save_encodings(data)

        return jsonify({"success": True, "message": f"{name} deleted"})

    return jsonify({"success": False, "message": "Student not found"})

# ---------------- DOWNLOAD ----------------
@app.route("/download")
def download():
    return send_file(ATTENDANCE_FILE, as_attachment=True)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)