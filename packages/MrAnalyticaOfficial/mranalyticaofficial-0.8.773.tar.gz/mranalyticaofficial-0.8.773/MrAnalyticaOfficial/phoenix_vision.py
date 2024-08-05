import cv2
import os
import numpy as np
import time
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf
from mtcnn import MTCNN
from tensorflow.keras.models import load_model

class PhoenixVision:
    def __init__(self, training_data_dir='training_data', model_path='facenet_model.h5'):
        self.training_data_dir = training_data_dir
        self.model_path = model_path
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.detector = MTCNN()
        self.facenet = load_model('facenet_keras.h5')
        self.classifier = SVC(kernel='linear', probability=True)
        self.label_encoder = LabelEncoder()
        self.training_duration = 60  # Default duration in seconds
        self.labels = []

    def preprocess_face(self, face):
        face = cv2.resize(face, (160, 160))
        face = face.astype('float32')
        mean, std = face.mean(), face.std()
        face = (face - mean) / std
        face = np.expand_dims(face, axis=0)
        return face

    def embed_face(self, face):
        face = self.preprocess_face(face)
        embedding = self.facenet.predict(face)
        return embedding

    def train_model(self):
        X = []
        y = []
        for root, dirs, files in os.walk(self.training_data_dir):
            for file in files:
                if file.endswith('.png'):
                    path = os.path.join(root, file)
                    face_img = cv2.imread(path)
                    faces = self.detector.detect_faces(face_img)
                    for face in faces:
                        x, y, width, height = face['box']
                        face_crop = face_img[y:y+height, x:x+width]
                        embedding = self.embed_face(face_crop)
                        X.append(embedding[0])
                        label = os.path.basename(root)
                        y.append(label)
        X = np.array(X)
        y = np.array(y)
        self.labels = list(set(y))
        y = self.label_encoder.fit_transform(y)
        self.classifier.fit(X, y)

    def save_model(self):
        np.save('labels.npy', self.label_encoder.classes_)
        with open('classifier.pkl', 'wb') as f:
            pickle.dump(self.classifier, f)

    def load_model(self):
        self.label_encoder.classes_ = np.load('labels.npy')
        with open('classifier.pkl', 'rb') as f:
            self.classifier = pickle.load(f)

    def TimeRecognize(self, minutes):
        self.training_duration = minutes * 60

    def recognize(self):
        while True:
            name = input("Nome da pessoa: ")
            if not name:
                continue

            # Crie a pasta se ela não existir
            person_folder = os.path.join(self.training_data_dir, name)
            if not os.path.exists(person_folder):
                os.makedirs(person_folder)

            cap = cv2.VideoCapture(0)
            start_time = time.time()
            count = 0

            while time.time() - start_time < self.training_duration:
                elapsed_time = time.time() - start_time
                remaining_time = self.training_duration - elapsed_time
                minutes = int(remaining_time // 60)
                seconds = int(remaining_time % 60)
                timer_text = f'Tempo restante: {minutes:02}:{seconds:02}'

                ret, frame = cap.read()
                if not ret:
                    continue
                faces = self.detector.detect_faces(frame)

                for face in faces:
                    x, y, width, height = face['box']
                    face_crop = frame[y:y+height, x:x+width]
                    face_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
                    embedding = self.embed_face(face_crop)

                    # Salve a imagem na pasta da pessoa
                    image_path = os.path.join(person_folder, f'{name}_{count}.png')
                    cv2.imwrite(image_path, face_crop)
                    count += 1

                    time.sleep(0.1)

                # Exibir o timer na tela
                cv2.putText(frame, timer_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
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

        # Treinar e salvar o modelo novamente após a captura
        self.train_model()
        self.save_model()

    def start(self):
        if not os.path.exists('labels.npy') or not os.path.exists('classifier.pkl'):
            self.train_model()
            self.save_model()
        else:
            self.load_model()

        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            faces = self.detector.detect_faces(frame)

            for face in faces:
                x, y, width, height = face['box']
                face_crop = frame[y:y+height, x:x+width]
                face_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
                embedding = self.embed_face(face_crop)

                predictions = self.classifier.predict_proba(embedding)
                best_idx = np.argmax(predictions, axis=1)[0]
                label = self.label_encoder.inverse_transform([best_idx])[0]
                confidence = predictions[0][best_idx] * 100

                label_with_confidence = f"{label} {confidence:.2f}%"
                cv2.putText(frame, label_with_confidence, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 2)

            cv2.imshow('Reconhecimento Facial', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
