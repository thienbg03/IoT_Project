from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
from routes.dht11_routes import dht11_blueprint

from modules.email import send_email  # Import the send_email function
from threading import Thread


# Initialize the Flask application
app = Flask(__name__)

app.register_blueprint(dht11_blueprint)

# Set up GPIO
led_pin = 17  # Define the GPIO pin number for the LED
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(led_pin, GPIO.OUT)  # Set the pin as an output
GPIO.output(led_pin, GPIO.LOW)  # Start with the LED turned off

# Initial LED state
LED_STATE = 'OFF'  # Variable to track the current state of the LED

@app.route('/')
def index():
    # """Render the main dashboard with the current LED state."""
    #send_email_trigger(28)
    return render_template('index.html', led_state=LED_STATE)

@app.route('/toggle_led', methods=['POST'])
def toggle_led():
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

@app.route('/cleanup', methods=['GET'])
def cleanup():
    """Clean up the GPIO pins. It doesn't work for some reason"""
    GPIO.cleanup()  # Reset the GPIO pins to their default state
    return "GPIO cleanup done."  # Confirmation message

def send_email_trigger(temperature):
    recipient = 'santisinsight@gmail.com'

    # Run send_email in a separate thread
    email_thread = Thread(target=send_email, args=(recipient, temperature))
    email_thread.start()

    # Immediately return a response while the email is being sent
    return jsonify({'message': 'Email is being sent.'}), 202

# Replace with your Raspberry Pi's IP address if necessary
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)  # Run the Flask application
