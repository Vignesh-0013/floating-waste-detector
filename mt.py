from gpiozero import Motor
from time import sleep

# L298N connections
motor = Motor(forward=17, backward=27)

try:
    while True:
        print("Anticlockwise")
        motor.backward()
        sleep(3)

        print("Clockwise")
        motor.forward()
        sleep(3)

except KeyboardInterrupt:
    print("Stopping motor")
    motor.stop()



#sudo apt update
#sudo apt install python3-gpiozero
