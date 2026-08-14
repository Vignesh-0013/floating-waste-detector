
import cv2
import numpy as np
import time
from gpiozero import Motor


# ============================================================
# DRIVE MOTORS - L298N #1
# ============================================================

left_motor = Motor(forward=17, backward=27)
right_motor = Motor(forward=22, backward=23)


# ============================================================
# CONVEYOR MOTOR - L298N #2
# GPIO24 -> IN1
# GPIO25 -> IN2
# ============================================================

conveyor_motor = Motor(forward=24, backward=25)


# ============================================================
# DRIVE MOTOR FUNCTIONS
# ============================================================

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
    left_motor.forward()
    right_motor.backward()


# ============================================================
# CONVEYOR FUNCTIONS
# ============================================================

def conveyor_on():
    # Conveyor runs BACKWARD
    conveyor_motor.backward()


def conveyor_off():
    conveyor_motor.stop()


# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Floating Waste Robot Started")
print("Press 'q' to quit.")


# ============================================================
# VARIABLES
# ============================================================

last_command = ""
last_time = 0


# ============================================================
# CONVEYOR SETTINGS
# ============================================================

# Conveyor runs for 16 seconds
CONVEYOR_TIME = 16

# Conveyor trigger line position
# 0.80 = 80% down the camera frame
CONVEYOR_LINE_POSITION = 0.80


# Conveyor state
conveyor_running = False
conveyor_start_time = 0


# ------------------------------------------------------------
# IMPORTANT:
# Prevents the same object from repeatedly starting
# the conveyor.
# ------------------------------------------------------------

conveyor_triggered = False


# ============================================================
# MAIN PROGRAM
# ============================================================

try:

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Camera frame error.")
            break


        # ====================================================
        # REMOVE MIRROR EFFECT
        # ====================================================

        frame = cv2.flip(frame, 1)


        # ====================================================
        # IMAGE SIZE
        # ====================================================

        height, width, _ = frame.shape

        frame_center_x = width // 2


        # ====================================================
        # CONVEYOR TRIGGER LINE
        # ====================================================

        conveyor_line_y = int(
            height * CONVEYOR_LINE_POSITION
        )


        # ====================================================
        # CONVEYOR RUNNING
        # ====================================================

        if conveyor_running:

            # Drive motors remain stopped
            stop_motors()

            # Conveyor runs backward
            conveyor_on()

            elapsed_time = (
                time.time()
                -
                conveyor_start_time
            )

            remaining_time = (
                CONVEYOR_TIME
                -
                elapsed_time
            )


            # Display countdown
            cv2.putText(
                frame,
                f"CONVEYOR BACKWARD: "
                f"{max(0, remaining_time):.1f}s",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )


            # ------------------------------------------------
            # 16 SECONDS COMPLETED
            # ------------------------------------------------

            if elapsed_time >= CONVEYOR_TIME:

                conveyor_off()

                conveyor_running = False

                print("CONVEYOR STOPPED")
                print("Waiting for object to clear...")


            # Display
            cv2.imshow(
                "Water Waste Robot",
                frame
            )


            if 'mask' in locals():

                cv2.imshow(
                    "Yellow Mask",
                    mask
                )


            # Quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


            # Don't perform normal movement
            continue


        # ====================================================
        # CENTER LINE
        # ====================================================

        cv2.line(
            frame,
            (frame_center_x, 0),
            (frame_center_x, height),
            (255, 0, 0),
            3
        )


        # ====================================================
        # CONVEYOR HORIZONTAL TRIGGER LINE
        # ====================================================

        cv2.line(
            frame,
            (0, conveyor_line_y),
            (width, conveyor_line_y),
            (0, 0, 255),
            3
        )


        cv2.putText(
            frame,
            "CONVEYOR LINE",
            (20, conveyor_line_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )


        # ====================================================
        # HSV
        # ====================================================

        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV
        )


        # ====================================================
        # YELLOW RANGE
        # ====================================================

        lower_yellow = np.array(
            [20, 100, 100]
        )

        upper_yellow = np.array(
            [35, 255, 255]
        )


        # ====================================================
        # MASK
        # ====================================================

        mask = cv2.inRange(
            hsv,
            lower_yellow,
            upper_yellow
        )


        # ====================================================
        # REMOVE NOISE
        # ====================================================

        kernel = np.ones(
            (5, 5),
            np.uint8
        )


        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel
        )


        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel
        )


        # ====================================================
        # FIND CONTOURS
        # ====================================================

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )


        object_found = False


        # ====================================================
        # CHECK OBJECT
        # ====================================================

        for cnt in contours:

            area = cv2.contourArea(cnt)


            # Ignore small noise
            if area > 500:

                object_found = True


                # =================================================
                # BOUNDING BOX
                # =================================================

                x, y, w, h = cv2.boundingRect(cnt)


                # =================================================
                # OBJECT CENTER
                # =================================================

                object_center_x = (
                    x + w // 2
                )

                object_center_y = (
                    y + h // 2
                )


                # =================================================
                # OBJECT BOTTOM
                # =================================================

                object_bottom_y = y + h


                # =================================================
                # DRAW BOUNDING BOX
                # =================================================

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )


                # =================================================
                # OBJECT CENTER
                # =================================================

                cv2.circle(
                    frame,
                    (
                        object_center_x,
                        object_center_y
                    ),
                    7,
                    (0, 0, 255),
                    -1
                )


                # =================================================
                # OBJECT BOTTOM POINT
                # =================================================

                cv2.circle(
                    frame,
                    (
                        object_center_x,
                        object_bottom_y
                    ),
                    7,
                    (255, 0, 255),
                    -1
                )


                # =================================================
                # SHOW BOTTOM POSITION
                # =================================================

                cv2.putText(
                    frame,
                    f"Bottom: {object_bottom_y}",
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 0),
                    2
                )


                # =================================================
                # ERROR FROM CENTER
                # =================================================

                error = (
                    object_center_x
                    -
                    frame_center_x
                )


                cv2.putText(
                    frame,
                    f"Error: {error}",
                    (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )


                # =================================================
                # CONVEYOR TRIGGER
                # =================================================

                if (
                    object_bottom_y >= conveyor_line_y
                    and
                    not conveyor_triggered
                ):

                    # ---------------------------------------------
                    # OBJECT REACHED CONVEYOR
                    # ---------------------------------------------

                    command = (
                        "CONVEYOR BACKWARD - 16 SEC"
                    )


                    # Stop drive motors
                    stop_motors()


                    # Start conveyor backward
                    conveyor_on()


                    # Start timer
                    conveyor_running = True

                    conveyor_start_time = (
                        time.time()
                    )


                    # Lock this object
                    conveyor_triggered = True


                    print(
                        "OBJECT REACHED CONVEYOR LINE"
                    )

                    print(
                        "DRIVE MOTORS STOPPED"
                    )

                    print(
                        "CONVEYOR RUNNING BACKWARD"
                    )

                    print(
                        "CONVEYOR WILL RUN FOR 16 SECONDS"
                    )


                # =================================================
                # OBJECT HAS NOT REACHED CONVEYOR
                # =================================================

                else:

                    # ---------------------------------------------
                    # OBJECT HAS MOVED AWAY
                    #
                    # Unlock conveyor for next object
                    # ---------------------------------------------

                    if (
                        object_bottom_y
                        <
                        conveyor_line_y - 30
                    ):

                        conveyor_triggered = False


                    # ---------------------------------------------
                    # OBJECT LEFT
                    # ---------------------------------------------

                    if error < -100:

                        command = "MOVE LEFT"

                        move_left()

                        conveyor_off()


                    # ---------------------------------------------
                    # OBJECT RIGHT
                    # ---------------------------------------------

                    elif error > 100:

                        command = "MOVE RIGHT"

                        move_right()

                        conveyor_off()


                    # ---------------------------------------------
                    # OBJECT CENTER
                    # ---------------------------------------------

                    else:

                        command = "MOVE FORWARD"

                        move_forward()

                        conveyor_off()


                # =================================================
                # PRINT COMMAND
                # =================================================

                current_time = time.time()


                if (
                    command != last_command
                    or
                    (
                        current_time
                        -
                        last_time
                    ) >= 1
                ):

                    print(command)

                    last_command = command

                    last_time = current_time


                # =================================================
                # DISPLAY COMMAND
                # =================================================

                cv2.putText(
                    frame,
                    command,
                    (50, 140),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    3
                )


                break


        # ====================================================
        # NO OBJECT FOUND
        # ====================================================

        if not object_found:

            command = "SEARCH"


            # Search for object
            search_object()


            # Conveyor OFF
            conveyor_off()


            # -----------------------------------------------
            # If object disappeared, unlock conveyor.
            #
            # This prevents an old object from keeping
            # the conveyor locked forever.
            # -----------------------------------------------

            conveyor_triggered = False


            current_time = time.time()


            if (
                command != last_command
                or
                (
                    current_time
                    -
                    last_time
                ) >= 1
            ):

                print(command)

                last_command = command

                last_time = current_time


            cv2.putText(
                frame,
                "SEARCH",
                (50, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )


        # ====================================================
        # DISPLAY
        # ====================================================

        cv2.imshow(
            "Water Waste Robot",
            frame
        )

        cv2.imshow(
            "Yellow Mask",
            mask
        )


        # ====================================================
        # QUIT
        # ====================================================

        if cv2.waitKey(1) & 0xFF == ord('q'):

            break


# ============================================================
# SAFETY STOP
# ============================================================

finally:

    print("Stopping all motors...")

    stop_motors()

    conveyor_off()

    cap.release()

    cv2.destroyAllWindows()
