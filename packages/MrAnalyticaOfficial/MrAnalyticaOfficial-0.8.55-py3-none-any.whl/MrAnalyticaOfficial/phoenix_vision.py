import cv2
import os
import numpy as np
import time

class PhoenixVision:
    def __init__(self, training_data_dir='training_data'):
        self.training_data_dir = training_data_dir
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.FisherFaceRecognizer_create()
        self.labels = {}
        self.load_training_data()

    def load_training_data(self):
        if not os.path.exists(self.training_data_dir):
            os.makedirs(self.training_data_dir)

        image_paths = [os.path.join(self.training_data_dir, f) for f in os.listdir(self.training_data_dir) if f.endswith('.png')]
        faces = []
        ids = []

        for image_path in image_paths:
            face_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            faces.append(face_img)

            label = os.path.splitext(os.path.basename(image_path))[0].split('_')[0]
            if label in self.labels:
                id_ = self.labels[label]
            else:
                id_ = len(self.labels)
                self.labels[label] = id_
            ids.append(id_)

        if len(faces) > 0:
            self.recognizer.train(faces, np.array(ids))

    def recognize(self, duration=60):
        while True:
            name = input("Nome da pessoa: ")
            if not name:
                continue

            cap = cv2.VideoCapture(0)
            start_time = time.time()
            count = 0

            while time.time() - start_time < duration:
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detectando faces com parâmetros ajustados
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60))

                for (x, y, w, h) in faces:
                    # Verificando a proporção para evitar a captura de olhos
                    aspect_ratio = w / h
                    if 0.8 <= aspect_ratio <= 1.2:
                        roi_gray = gray[y:y+h, x:x+w]
                        resized_face = cv2.resize(roi_gray, (200, 200))
                        resized_face = cv2.equalizeHist(resized_face)

                        image_path = os.path.join(self.training_data_dir, f'{name}_{count}.png')
                        cv2.imwrite(image_path, resized_face)
                        count += 1

                        time.sleep(0.1) 

                cv2.imshow('Capturando rosto...', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

            print(f"{name} salvo com sucesso!")

            # Perguntar se o usuário deseja continuar o treinamento
            choice = input("Deseja treinar outra pessoa? (1 - Sim, 2 - Não): ")
            if choice == '2':
                break

    def start(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=6)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                
                # Redimensionando a ROI para o mesmo tamanho usado no treinamento
                roi_gray = cv2.resize(roi_gray, (200, 200))
                
                roi_gray = cv2.equalizeHist(roi_gray)
                
                id_, confidence = self.recognizer.predict(roi_gray)

                if confidence < 90:
                    label = list(self.labels.keys())[list(self.labels.values()).index(id_)]
                    cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow('Reconhecimento Facial', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()