from ultralytics import YOLO
import cv2
import numpy as np

class ParkingDetector:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        self.vehicle_classes = ['car', 'bus', 'truck', 'motorcycle']

    def detect(self, image_bytes):
        # Отладочный вывод
        print(f"Получено байт: {len(image_bytes)}")
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            print("ОШИБКА: не удалось декодировать изображение")
            return {'vehicles': [], 'count': 0, 'annotated_image': np.zeros((100,100,3), dtype=np.uint8)}

        print(f"Размер изображения: {img.shape}")
        results = self.model(img, conf=0.1)  # сниженный порог для теста
        print(f"Всего объектов обнаружено: {len(results[0].boxes)}")

        detected_vehicles = []
        for box in results[0].boxes:
            cls = int(box.cls[0])
            class_name = self.model.names[cls]
            conf = float(box.conf[0])
            print(f"Найден объект: {class_name}, уверенность: {conf:.2f}")
            if class_name in self.vehicle_classes:
                detected_vehicles.append({
                    'class': class_name,
                    'confidence': conf,
                    'bbox': box.xyxy[0].tolist()
                })

        print(f"Отфильтровано машин: {len(detected_vehicles)}")
        annotated_img = results[0].plot()
        return {
            'vehicles': detected_vehicles,
            'count': len(detected_vehicles),
            'annotated_image': annotated_img
        }