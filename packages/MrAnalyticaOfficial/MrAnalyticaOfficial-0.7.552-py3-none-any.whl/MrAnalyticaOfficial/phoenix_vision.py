import cv2
import os
import numpy as np
import time
import random
import psutil

class PhoenixVision:
    def __init__(self, fotos_dir):
        self.fotos_dir = fotos_dir
        self.rostos = []
        self.labels = []
        self.names = []
        self.show_certainty = False
        self.show_stats = False
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.detection_mode = "face"
        self.resolution = (640, 480)  # Default resolution
        self.face_tracking = False
        self.camera_index = 0
        self.tracker = cv2.TrackerKCF_create()
        self._carregar_fotos()
        self._treinar()
        self.frame_count = 0
        self.start_time = time.time()
        self.total_faces_detected = 0

    def _carregar_fotos(self):
        label_id = 0
        for nome_pessoa in os.listdir(self.fotos_dir):
            pessoa_path = os.path.join(self.fotos_dir, nome_pessoa)
            if os.path.isdir(pessoa_path):
                for nome_imagem in os.listdir(pessoa_path):
                    imagem_path = os.path.join(pessoa_path, nome_imagem)
                    imagem = cv2.imread(imagem_path)
                    gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
                    self.rostos.append(gray)
                    self.labels.append(label_id)
                self.names.append(nome_pessoa)
                label_id += 1

    def _treinar(self):
        self.recognizer.train(self.rostos, np.array(self.labels))

    def certainty(self, show=True):
        self.show_certainty = show

    def statsfornerds(self, show=True):
        self.show_stats = show

    def _draw_advanced_face_landmarks(self, frame, face):
        x, y, w, h = face
        center = (x + w // 2, y + h // 2)
        
        # Gerar pontos aleatórios ao redor do rosto
        num_points = 30
        points = [(random.randint(x, x+w), random.randint(y, y+h)) for _ in range(num_points)]
        
        # Desenhar pontos
        for point in points:
            cv2.circle(frame, point, 2, (0, 255, 255), -1)
        
        # Desenhar linhas conectando pontos próximos
        for i, point1 in enumerate(points):
            for point2 in points[i+1:]:
                distance = np.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
                if distance < w//3:  # Ajuste este valor para mais ou menos conexões
                    cv2.line(frame, point1, point2, (0, 255, 255), 1)
        
        # Desenhar círculo ao redor do rosto
        cv2.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (0, 255, 255), 1)
        
        # Adicionar efeito de "escaneamento"
        scan_height = int(self.frame_count % h)
        cv2.line(frame, (x, y + scan_height), (x + w, y + scan_height), (0, 255, 255), 1)

    def set_detection_mode(self, mode):
        valid_modes = ["face", "face_eyes", "face_full"]
        if mode not in valid_modes:
            raise ValueError(f"Modo inválido. Escolha entre: {', '.join(valid_modes)}")
        self.detection_mode = mode
        print(f"Modo de detecção alterado para: {mode}")

    def _detect_and_draw(self, frame, gray):
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=7, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            if self.detection_mode in ["face_eyes", "face_full"]:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            
            if self.detection_mode == "face_full":
                self._draw_advanced_face_landmarks(frame, (x, y, w, h))

        return faces
    
    def set_resolution(self, width, height):
        self.resolution = (width, height)
        print(f"Resolução definida para: {width}x{height}")

    def enable_face_tracking(self, enable):
        self.face_tracking = enable
        if enable:
            self.tracker = cv2.TrackerKCF_create()
            print("Rastreamento de rostos ativado")
        else:
            print("Rastreamento de rostos desativado")

    def set_camera(self, camera_index):
        self.camera_index = camera_index
        print(f"Câmera definida para índice: {camera_index}")

    def start(self):
        video_capture = cv2.VideoCapture(self.camera_index)
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

        tracking_face = False
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Falha ao capturar o frame")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if self.face_tracking and tracking_face:
                tracking_success, bbox = self.tracker.update(frame)
                if tracking_success:
                    x, y, w, h = [int(v) for v in bbox]
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    face_roi = gray[y:y+h, x:x+w]
                    id, confianca = self.recognizer.predict(face_roi)
                    self._display_recognition_result(frame, x, y, id, confianca)
                else:
                    tracking_face = False

            if not self.face_tracking or not tracking_face:
                faces = self._detect_and_draw(frame, gray)
                for (x, y, w, h) in faces:
                    face_roi = gray[y:y+h, x:x+w]
                    id, confianca = self.recognizer.predict(face_roi)
                    if confianca < 50:  # Ajuste de confiança mínima
                        self._display_recognition_result(frame, x, y, id, confianca)
                
                if len(faces) > 0 and self.face_tracking:
                    x, y, w, h = faces[0]
                    self.tracker = cv2.TrackerKCF_create()
                    self.tracker.init(frame, (x, y, w, h))
                    tracking_face = True

            self.frame_count += 1
            elapsed_time = time.time() - self.start_time
            fps = self.frame_count / elapsed_time
            self.total_faces_detected += len(faces)

            if self.show_stats:
                stats_text = [
                    f"Modo: {self.detection_mode}",
                    f"Resolução: {self.resolution[0]}x{self.resolution[1]}",
                    f"Câmera: {self.camera_index}",
                    f"Rastreamento: {'Ativado' if self.face_tracking else 'Desativado'}",
                    f"FPS: {fps:.2f}",
                    f"Faces detectadas: {len(faces)}",
                    f"Total de faces detectadas: {self.total_faces_detected}",
                    f"Tempo decorrido: {elapsed_time:.2f}s",
                    f"Memória usada: {self._get_memory_usage():.2f} MB"
                ]
                for i, text in enumerate(stats_text):
                    cv2.putText(frame, text, (10, 30 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

    def _display_recognition_result(self, frame, x, y, id, confianca):
        if 0 <= id < len(self.names):
            nome = self.names[id]
            texto = nome
            if self.show_certainty:
                texto += f' ({100 - int(confianca)}%)'
            if confianca < 50:  # Ajuste de confiança mínima
                cv2.putText(frame, texto, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Desconhecido", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Desconhecido", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    def _get_memory_usage(self):
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  # em MB
