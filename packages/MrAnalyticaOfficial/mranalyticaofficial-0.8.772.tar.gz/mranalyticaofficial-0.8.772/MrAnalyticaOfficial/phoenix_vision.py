import cv2
import os
import numpy as np
import time

class PhoenixVision:
    def __init__(self, training_data_dir='training_data', model_path='trained_model.xml'):
        self.training_data_dir = training_data_dir
        self.model_path = model_path
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.FisherFaceRecognizer_create()
        self.labels = {}
        self.training_duration = 60  # Default duration in seconds

        if os.path.exists(self.model_path):
            self.load_model()
        else:
            self.load_training_data()
            self.train_model()
            self.save_model()

    def load_training_data(self):
        if not os.path.exists(self.training_data_dir):
            os.makedirs(self.training_data_dir)

        image_paths = []
        for root, dirs, files in os.walk(self.training_data_dir):
            for file in files:
                if file.endswith('.png'):
                    image_paths.append(os.path.join(root, file))

        faces = []
        ids = []

        for image_path in image_paths:
            face_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            faces.append(face_img)

            label = os.path.basename(os.path.dirname(image_path))
            if label in self.labels:
                id_ = self.labels[label]
            else:
                id_ = len(self.labels)
                self.labels[label] = id_
            ids.append(id_)

        if len(faces) > 0:
            self.recognizer.train(faces, np.array(ids))

    def train_model(self):
        image_paths = []
        for root, dirs, files in os.walk(self.training_data_dir):
            for file in files:
                if file.endswith('.png'):
                    image_paths.append(os.path.join(root, file))

        faces = []
        ids = []

        for image_path in image_paths:
            face_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            faces.append(face_img)

            label = os.path.basename(os.path.dirname(image_path))
            if label in self.labels:
                id_ = self.labels[label]
            else:
                id_ = len(self.labels)
                self.labels[label] = id_
            ids.append(id_)

        if len(faces) > 0:
            self.recognizer.train(faces, np.array(ids))

    def save_model(self):
        self.recognizer.write(self.model_path)
        with open(self.model_path.replace('.xml', '_labels.txt'), 'w') as f:
            for name, id_ in self.labels.items():
                f.write(f'{name}:{id_}\n')

    def load_model(self):
        self.recognizer.read(self.model_path)
        with open(self.model_path.replace('.xml', '_labels.txt'), 'r') as f:
            for line in f:
                name, id_ = line.strip().split(':')
                self.labels[name] = int(id_)

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
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detectando faces com parâmetros ajustados
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60))

                for (x, y, w, h) in faces:
                    # Verificando a proporção para evitar a captura de olhos
                    aspect_ratio = w / h
                    if 0.8 <= aspect_ratio <= 1.2:
                        roi_gray = gray[y:y+h, x:x+w]  # Corrigido aqui
                        resized_face = cv2.resize(roi_gray, (200, 200))
                        resized_face = cv2.equalizeHist(resized_face)

                        # Salve a imagem na pasta da pessoa
                        image_path = os.path.join(person_folder, f'{name}_{count}.png')
                        cv2.imwrite(image_path, resized_face)
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
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=6)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]  # Corrigido aqui
                roi_gray = cv2.resize(roi_gray, (200, 200))
                roi_gray = cv2.equalizeHist(roi_gray)

                id_, confidence = self.recognizer.predict(roi_gray)

                if confidence < 90:
                    label = list(self.labels.keys())[list(self.labels.values()).index(id_)]
                    confidence_percentage = round(100 - confidence)  # Calcula a porcentagem de confiança
                    label_with_confidence = f"{label} {confidence_percentage}%"  # Concatena o nome com a porcentagem

                    cv2.putText(frame, label_with_confidence, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow('Reconhecimento Facial', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
