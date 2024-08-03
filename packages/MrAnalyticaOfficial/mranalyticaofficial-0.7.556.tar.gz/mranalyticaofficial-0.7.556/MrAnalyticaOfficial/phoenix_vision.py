import cv2
import os
import numpy as np
import time

class PhoenixVision:
    def __init__(self, training_data_dir='training_data'):
        self.training_data_dir = training_data_dir
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.labels = {}
        self.load_training_data()

    def load_training_data(self):
        if not os.path.exists(self.training_data_dir):
            os.makedirs(self.training_data_dir)

        image_paths = [os.path.join(self.training_data_dir, f) for f in os.listdir(self.training_data_dir) if f.endswith('.npy')]
        faces = []
        ids = []

        for image_path in image_paths:
            face_img = np.load(image_path)

            # Correção: Converter para escala de cinza
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)

            faces.append(face_img)
            label = os.path.splitext(os.path.basename(image_path))[0]
            if label in self.labels:
                id_ = self.labels[label]
            else:
                id_ = len(self.labels)
                self.labels[label] = id_
            ids.append(id_)

        if len(faces) > 0:
            self.recognizer.train(faces, np.array(ids))

    def recognize(self, duration=30):
        name = input("Nome da pessoa: ")
        if not name:
            return

        cap = cv2.VideoCapture(0)
        start_time = time.time()
        faces_captured = []

        while time.time() - start_time < duration:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                resized_face = cv2.resize(roi_gray, (200, 200))
                faces_captured.append(resized_face)

            cv2.imshow('Capturando rosto...', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if faces_captured:
            face_array = np.array(faces_captured)
            np.save(os.path.join(self.training_data_dir, f'{name}.npy'), face_array)
            print(f"{name} salvo com sucesso!")

    def start(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                id_, confidence = self.recognizer.predict(roi_gray)

                if confidence < 70:
                    label = list(self.labels.keys())[list(self.labels.values()).index(id_)]
                    cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow('Reconhecimento Facial', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()