from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("best.pt")

# Open webcam
cap = cv2.VideoCapture(0)

# Set low resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Reduce camera buffer (helps reduce lag)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 'q' to quit.")

frame_count = 0
annotated_frame = None

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break

    frame_count += 1

    # Run YOLO every 2nd frame
    if frame_count % 2 == 0:

        results = model.predict(
            source=frame,
            imgsz=320,      # Smaller input size
            conf=0.4,
            verbose=False
        )

        annotated_frame = results[0].plot()

    # Display latest processed frame
    if annotated_frame is not None:
        cv2.imshow("YOLO Live Detection", annotated_frame)
    else:
        cv2.imshow("YOLO Live Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
