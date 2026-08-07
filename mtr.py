import cv2
import numpy as np
import time
from gpiozero import Motor

# -----------------------------
# Motor Setup
# -----------------------------
left_motor = Motor(forward=17, backward=27)
right_motor = Motor(forward=22, backward=23)

def move_forward():
    left_motor.forward()
    right_motor.forward()

def move_left():
    left_motor.backward()
    right_motor.forward()

def move_right():
    left_motor.forward()
    right_motor.backward()

def stop_motors():
    left_motor.stop()
    right_motor.stop()

def search_object():
    # Rotate in place
    left_motor.forward()
    right_motor.backward()

# -----------------------------
# Camera
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 'q' to quit.")

last_command = ""
last_time = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    height, width, _ = frame.shape

    frame_center_x = width // 2

    cv2.line(frame,
             (frame_center_x, 0),
             (frame_center_x, height),
             (255, 0, 0),
             3)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([35,255,255])

    mask = cv2.inRange(hsv,
                       lower_yellow,
                       upper_yellow)

    kernel = np.ones((5,5), np.uint8)

    mask = cv2.morphologyEx(mask,
                            cv2.MORPH_OPEN,
                            kernel)

    mask = cv2.morphologyEx(mask,
                            cv2.MORPH_CLOSE,
                            kernel)

    contours, _ = cv2.findContours(mask,
                                   cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    object_found = False

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area > 500:

            object_found = True

            x, y, w, h = cv2.boundingRect(cnt)

            object_center_x = x + w//2
            object_center_y = y + h//2

            cv2.rectangle(frame,
                          (x,y),
                          (x+w,y+h),
                          (0,255,0),
                          2)

            cv2.circle(frame,
                       (object_center_x, object_center_y),
                       7,
                       (0,0,255),
                       -1)

            error = object_center_x - frame_center_x

            cv2.putText(frame,
                        f"Error: {error}",
                        (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0,255,255),
                        2)

            tolerance = 100

            if error < -tolerance:

                command = "MOVE LEFT"
                move_left()

            elif error > tolerance:

                command = "MOVE RIGHT"
                move_right()

            else:

                if area < 8000:

                    command = "MOVE FORWARD"
                    move_forward()

                else:

                    command = "STOP"
                    stop_motors()

            current_time = time.time()

            if command != last_command or (current_time-last_time)>=1:
                print(command)
                last_command = command
                last_time = current_time

            cv2.putText(frame,
                        command,
                        (50,90),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,255,0),
                        3)

            break

    if not object_found:

        command = "SEARCH"

        search_object()

        current_time = time.time()

        if command != last_command or (current_time-last_time)>=1:
            print(command)
            last_command = command
            last_time = current_time

        cv2.putText(frame,
                    command,
                    (50,90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    3)

    cv2.imshow("Water Waste Robot", frame)
    cv2.imshow("Yellow Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

stop_motors()

cap.release()
cv2.destroyAllWindows()
