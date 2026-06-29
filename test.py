from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("best.pt")

# Open webcam (0 = default webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break

    # Run YOLO inference
    results = model.predict(
        source=frame,
        conf=0.4,
        verbose=False
    )

    # Draw bounding boxes
    annotated_frame = results[0].plot()

    # Display output
    cv2.imshow("YOLO Live Detection", annotated_frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()