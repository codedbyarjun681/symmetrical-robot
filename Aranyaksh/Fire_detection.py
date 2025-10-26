import cv2
from ultralytics import YOLO

model = YOLO('best.pt')

cap = cv2.VideoCapture(0) 

print("Starting Fire Detection Module... Press 'q' to exit.")

while True:
    success, frame = cap.read()

    if success:
        results = model(frame)

        annotated_frame = results[0].plot()

        if len(results[0].boxes) > 0:
            print("!!! ALERT: FIRE DETECTED! Sending alert to ground team... !!!")

        cv2.imshow("YOLOv8 Fire Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()