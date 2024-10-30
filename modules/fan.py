import RPi.GPIO as GPIO
from time import sleep

def turn_off_fan():
    # Set up GPIO mode and suppress warnings
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Define GPIO pin assignments
    Motor1 = 22  # Enable Pin
    Motor2 = 27  # Input Pin
    Motor3 = 17  # Input Pin

    # Set up GPIO pins as output
    GPIO.setup(Motor1, GPIO.OUT)
    GPIO.setup(Motor2, GPIO.OUT)
    GPIO.setup(Motor3, GPIO.OUT)

    # Initial motor control logic
    GPIO.output(Motor1, GPIO.LOW)
    GPIO.output(Motor2, GPIO.LOW)
    GPIO.output(Motor3, GPIO.LOW)
    print("Turning off fan")

def turn_on_fan():
    # Set up GPIO mode and suppress warnings
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Define GPIO pin assignments
    Motor1 = 22  # Enable Pin
    Motor2 = 27  # Input Pin
    Motor3 = 17  # Input Pin

    # Set up GPIO pins as output
    GPIO.setup(Motor1, GPIO.OUT)
    GPIO.setup(Motor2, GPIO.OUT)
    GPIO.setup(Motor3, GPIO.OUT)
    
    # Initial motor control logic
    GPIO.output(Motor1, GPIO.HIGH)
    GPIO.output(Motor2, GPIO.LOW)
    GPIO.output(Motor3, GPIO.HIGH)
    print("Turning on fan")

