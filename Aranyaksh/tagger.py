import cv2
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, animal_model_path, fire_model_path):
        try:
            self.animal_model = YOLO(animal_model_path)
            self.animal_class_names = self.animal_model.names
            self.fire_model = YOLO(fire_model_path)
            self.fire_class_names = self.fire_model.names
        except Exception as e:
            raise Exception(f"Failed to load models: {e}")
        
        self.confidence_threshold = 0.70
        self.animal_box_color = (255, 0, 255)
        self.fire_box_color = (0, 0, 255)

    def process_frame(self, frame):
        frame_detections = []
        all_results = []

        animal_results = self.animal_model(frame, stream=True, verbose=False)
        for r in animal_results:
            for box in r.boxes:
                if box.conf[0] >= self.confidence_threshold:
                    all_results.append((box, self.animal_class_names, self.animal_box_color))

        fire_results = self.fire_model(frame, stream=True, verbose=False)
        for r in fire_results:
            for box in r.boxes:
                if box.conf[0] >= self.confidence_threshold:
                    all_results.append((box, self.fire_class_names, self.fire_box_color))

        for box, class_names, color in all_results:
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = class_names.get(class_id, "Unknown")
            
            frame_detections.append({
                "Object": class_name,
                "Confidence": f"{confidence:.2f}"
            })
            
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = f'{class_name} {confidence:.2f}'
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (x1, y1 - h - 10), (x1 + w, y1), color, -1)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame, frame_detections