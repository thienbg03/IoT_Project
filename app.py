from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
from routes.dht11_routes import dht11_blueprint
from modules.email import send_email, receive_email # Import the email functions
from modules.fan import turn_on_fan, turn_off_fan
from threading import Thread
from modules.DHT11 import DHT11Sensor  # Import the updated DHT11Sensor class

from threading import Thread

# Initialize the Flask application
app = Flask(__name__)

# simulation with fake data to see if the saving works:
# app.register_blueprint(dht11_blueprint)

# Set up GPIO
led_pin = 17  # Define the GPIO pin number for the LED
DHT_PIN = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(led_pin, GPIO.OUT)  # Set the pin as an output
GPIO.output(led_pin, GPIO.LOW)  # Start with the LED turned off

# Initial LED state
LED_STATE = 'OFF'  # Variable to track the current state of the LED

# Initialize the DHT11 sensor
sensor = DHT11Sensor(DHT_PIN)

@app.route('/')
def index():
    # """Render the main dashboard with the current LED state."""
    test_receive_email()
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

@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    # Retrieve temperature and humidity from the DHT11 sensor
    temperature, humidity = sensor.read_data()
    temperature = 25
    if temperature is not None and humidity is not None:
        sensor.save_data(temperature, humidity)  # Save the data to JSON
        if temperature > 24:
            send_email_trigger(temperature)
        return jsonify({'temperature': temperature, 'humidity': humidity})
    else:
        return jsonify({'error': 'Failed to read data from DHT11 sensor.'}), 500

def send_email_trigger(temperature):
    recipient = 'santisinsight@gmail.com'

    # Run send_email in a separate thread
    email_thread = Thread(target=send_email, args=(recipient, temperature))
    email_thread.start()

    # Immediately return a response while the email is being sent
    return jsonify({'message': 'Email is being sent.'}), 202

def test_receive_email():
    print("Receive email method is being called from app.py")
    
    def receive_and_check():
        result = receive_email()
        if result:  # Only call turn_on_fan if the email is received successfully
            turn_on_fan()

    email_thread = Thread(target=receive_and_check)
    email_thread.start()
    email_thread.join(5)  # Wait for 10 seconds

    if email_thread.is_alive():
        print("Function timed out after 5 seconds")

# Replace with your Raspberry Pi's IP address if necessary
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)  # Run the Flask application