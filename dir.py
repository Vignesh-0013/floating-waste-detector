from gpiozero import Motor
from time import sleep

# Left motor: OUT1 & OUT2
left_motor = Motor(forward=17, backward=27)

# Right motor: OUT3 & OUT4
right_motor = Motor(forward=22, backward=23)

print("Forward")
left_motor.forward()
right_motor.forward()
sleep(3)

print("Backward")
left_motor.backward()
right_motor.backward()
sleep(3)

print("Turn Left")
left_motor.backward()
right_motor.forward()
sleep(3)

print("Turn Right")
left_motor.forward()
right_motor.backward()
sleep(3)

print("Stop")
left_motor.stop()
right_motor.stop()
