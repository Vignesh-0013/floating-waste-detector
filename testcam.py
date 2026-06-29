import cv2

# Open default webcam (0)
cap = cv2.VideoCapture(0)

# Check if webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 'q' to quit.")

while True:
    # Read a frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame.")
        break

    # Display the frame
    cv2.imshow("Webcam", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam and close windows
cap.release()
cv2.destroyAllWindows()