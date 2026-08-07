from gpiozero import Motor
from time import sleep

left_motor = Motor(forward=17, backward=27)
right_motor = Motor(forward=22, backward=23)

# Test 1
print("LEFT FORWARD")
left_motor.forward()
sleep(3)
left_motor.stop()

sleep(2)

# Test 2
print("LEFT BACKWARD")
left_motor.backward()
sleep(3)
left_motor.stop()

sleep(2)

# Test 3
print("RIGHT FORWARD")
right_motor.forward()
sleep(3)
right_motor.stop()

sleep(2)

# Test 4
print("RIGHT BACKWARD")
right_motor.backward()
sleep(3)
right_motor.stop()

print("Finished")
