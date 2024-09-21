from flask import Flask, render_template, request, jsonify
# import RPi.GPIO as GPIO

# # Initialize the Flask application
app = Flask(__name__)

# # Set up GPIO
# led_pin = 17  # Define the GPIO pin number for the LED
# GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
# GPIO.setup(led_pin, GPIO.OUT)  # Set the pin as an output
# GPIO.output(led_pin, GPIO.LOW)  # Start with the LED turned off

# Initial LED state
LED_STATE = 'OFF'  # Variable to track the current state of the LED

@app.route('/')
def index():
    """Render the main dashboard with the current LED state."""
    return render_template('index.html', led_state=LED_STATE)

# @app.route('/toggle_led', methods=['POST'])
# def toggle_led():
#     """Toggle the LED state based on the request from the frontend."""
#     global LED_STATE  # Use the global variable to keep track of the LED state
6
#     # Get the state from the JSON request
#     data = request.get_json()
#     if data['state'] == 'ON':
#         GPIO.output(led_pin, GPIO.HIGH)  # Turn the LED on
#         LED_STATE = 'ON'  # Update the state variable
#     else:
#         GPIO.output(led_pin, GPIO.LOW)  # Turn the LED off
#         LED_STATE = 'OFF'  # Update the state variable

#     # Return the current LED state as JSON
#     return jsonify({'led_state': LED_STATE})

# @app.route('/cleanup', methods=['GET'])
# def cleanup():
#     """Clean up the GPIO pins. It doesn't work for some reason"""
#     GPIO.cleanup()  # Reset the GPIO pins to their default state
#     return "GPIO cleanup done."  # Confirmation message

# Replace with your Raspberry Pi's IP address if necessary
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # Run the Flask application
