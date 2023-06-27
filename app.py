from flask import Flask, request,render_template
# from bs4 import BeautifulSoup
from urllib.request import urlopen

app=Flask(__name__)

html=urlopen('file:///E:/F.R.A.S/sem 6/templates/index.htm')

@app.route("/")
def index():
    return render_template('index.htm');

@app.route('/move_forward')
def move_forward():
    import face_recognition
    import cv2
    import numpy as np
    import csv
    import os
    from datetime import datetime

    video_capture = cv2.VideoCapture(0)

    jobs_image = face_recognition.load_image_file("Jobs.jpg")
    jobs_encoding = face_recognition.face_encodings(jobs_image)[0]

    tata_image = face_recognition.load_image_file("Tata.jpg")
    tata_encoding = face_recognition.face_encodings(tata_image)[0]

    known_face_encoding = [
        jobs_encoding,
        tata_encoding,
    ]

    known_face_names = [
        "Jobs",
        "Tata"
    ]

    students = known_face_names.copy()

    face_locations = []
    face_encodings = []
    face_names = []
    s = True

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    f = open(current_date + '.csv', 'w+', newline='')
    lnwriter = csv.writer(f)
    lnwriter.writerow(["NAME", "CURRENT TIME", "ATTENDANCE"])

    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if s:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_name = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
                name = ""
                face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
                best_match_index = np.argmin(face_distance)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)

                if name in known_face_names:
                    if name in students:
                        students.remove(name)
                        print(":::Present:::", name)
                        now1 = datetime.now()
                        current_time = now1.strftime("%H-%M-%S")
                        lnwriter.writerow([name, current_time, "Present"])
                        print(current_time)
                        if students == []:
                            s = False
        cv2.imshow("F.R.A.S. : Attendance System", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    f.close()
    return render_template('result.html')
if(__name__ == '__main__'):
    app.run(debug=True,port=5000)