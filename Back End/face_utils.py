import cv2
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load
from datetime import datetime

FACE_DIR = 'static/faces'
MODEL_PATH = 'facenet_model.pkl'
CASCADE_PATH = 'haarcascade_frontalface_default.xml'

def train_model():
    X, y = [], []
    for person in os.listdir(FACE_DIR):
        person_path = os.path.join(FACE_DIR, person)
        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (50, 50)).flatten()
            X.append(img)
            y.append(person)
    if X:
        clf = KNeighborsClassifier(n_neighbors=3)
        clf.fit(X, y)
        dump(clf, MODEL_PATH)


class VideoCamera:
    def __init__(self, mode='detect', name=None):
        self.video = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
        self.mode = mode
        self.name = name
        self.counter = 0
        self.max_images = 100
        self.clf = load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
        self.finished = False

        if self.name:
            self.user_path = os.path.join(FACE_DIR, self.name)
            os.makedirs(self.user_path, exist_ok=True)

    def __del__(self):
        if self.video.isOpened():
            self.video.release()

    def get_frame_stream(self):
        while True:
            success, frame = self.video.read()
            if not success:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face, (50, 50))

                if self.mode == 'register' and self.counter < self.max_images:
                    filename = os.path.join(self.user_path, f'{self.counter}.png')
                    cv2.imwrite(filename, face_resized)
                    self.counter += 1

                    # Show progress bar
                    progress_text = f"Capturing {self.counter}/{self.max_images}"
                    cv2.putText(frame, progress_text, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                    if self.counter == self.max_images:
                        train_model()
                        self.finished = True

                if self.mode == 'detect' and self.clf:
                    face_flat = face_resized.flatten().reshape(1, -1)
                    label = self.clf.predict(face_flat)[0]
                    cv2.putText(frame, label, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Auto exit stream when registration is done
            if self.mode == 'register' and self.finished:
                self.__del__()
                break

            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                break

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            
            # Close camera after registration finishes
            if self.mode == 'register' and self.finished:
                self.video.release()
                break
