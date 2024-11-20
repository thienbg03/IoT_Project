import RPi.GPIO as GPIO

LED_STATE = 'OFF'  # Variable to track the current state of the LED

# Initial LED state
def setup_led():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    GPIO.setup(led_pin, GPIO.OUT)  # Set the pin as an output
    GPIO.output(led_pin, GPIO.LOW)  # Start with the LED turned off

    LED_STATE = 'OFF'  # Variable to track the current state of the LED

def toggle_led(led_pin, request):
    # """Toggle the LED state based on the request from the frontend."""
    global LED_STATE  # Use the global variable to keep track of the LED state

    # Get the state from the JSON request
    data = request.get_json()
    print(data['state'])
    if data['state'] == 'ON':
        GPIO.output(led_pin, GPIO.HIGH)  # Turn the LED on
        LED_STATE = 'ON'  # Update the state variable
    else:
        GPIO.output(led_pin, GPIO.LOW)  # Turn the LED off
        LED_STATE = 'OFF'  # Update the state variable

    # Return the current LED state as JSON
    return jsonify({'led_state': LED_STATE})