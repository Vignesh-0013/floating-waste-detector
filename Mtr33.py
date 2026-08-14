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
# DRIVE FUNCTIONS
# ============================================================

def move_forward():

    left_motor.forward()
    right_motor.forward()

    print("FORWARD")


def move_left():

    left_motor.backward()
    right_motor.forward()

    print("LEFT")


def move_right():

    left_motor.forward()
    right_motor.backward()

    print("RIGHT")


def stop_motors():

    left_motor.stop()
    right_motor.stop()

    print("DRIVE MOTORS STOPPED")


# ============================================================
# CONVEYOR FUNCTIONS
# ============================================================

def conveyor_backward():

    # Conveyor runs BACKWARD
    conveyor_motor.backward()

    print("CONVEYOR BACKWARD")


def conveyor_forward():

    conveyor_motor.forward()

    print("CONVEYOR FORWARD")


def conveyor_stop():

    conveyor_motor.stop()

    print("CONVEYOR STOPPED")


# ============================================================
# STOP EVERYTHING
# ============================================================

def stop_all():

    left_motor.stop()
    right_motor.stop()
    conveyor_motor.stop()


# ============================================================
# MAIN PROGRAM
# ============================================================

print("--------------------------------")
print("ROBOT MOTOR TEST")
print("--------------------------------")
print("f = Forward")
print("l = Left")
print("r = Right")
print("c = Conveyor Backward")
print("s = Stop")
print("q = Quit")
print("--------------------------------")


try:

    while True:

        command = input("Enter command: ").strip().lower()


        # ----------------------------------------------------
        # FORWARD
        # ----------------------------------------------------

        if command == "f":

            conveyor_stop()

            move_forward()


        # ----------------------------------------------------
        # LEFT
        # ----------------------------------------------------

        elif command == "l":

            conveyor_stop()

            move_left()


        # ----------------------------------------------------
        # RIGHT
        # ----------------------------------------------------

        elif command == "r":

            conveyor_stop()

            move_right()


        # ----------------------------------------------------
        # CONVEYOR BACKWARD
        # ----------------------------------------------------

        elif command == "c":

            stop_motors()

            conveyor_backward()


        # ----------------------------------------------------
        # STOP
        # ----------------------------------------------------

        elif command == "s":

            stop_all()

            print("ALL MOTORS STOPPED")


        # ----------------------------------------------------
        # QUIT
        # ----------------------------------------------------

        elif command == "q":

            print("Exiting...")

            break


        # ----------------------------------------------------
        # INVALID COMMAND
        # ----------------------------------------------------

        else:

            print("Invalid command.")
            print("Use: f, l, r, c, s, q")


finally:

    # SAFETY STOP
    stop_all()

    print("All motors stopped.")
