from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
from routes.dht11_routes import dht11_blueprint
from modules.fan import turn_on_fan, turn_off_fan
import threading
from modules.DHT11 import DHT11Sensor  # Import the updated DHT11Sensor class
from time import sleep
from modules.email_temp import send_email, receive_email # Import the send_email function
from modules.email_notifier import send_email_notification
from threading import Thread
# from modules.mqtt_subscriber import email_notifier


# Initialize the Flask application
app = Flask(__name__)

# simulation with fake data to see if the saving works:
# app.register_blueprint(dht11_blueprint)
# Set up GPIO
led_pin = 16  # Define the GPIO pin number for the LED
DHT_PIN = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Use BCM pin numbering
GPIO.setup(led_pin, GPIO.OUT)  # Set the pin as an output
GPIO.output(led_pin, GPIO.LOW) 

# Start with the LED turned off
# Initialize global states
LED_STATE = 'OFF'
FAN_STATE = 'OFF'
email_thread_running = False
# Initial LED statesudo apt-get install python3-rpi.gpio 
sensor = DHT11Sensor(DHT_PIN)

@app.route('/')
def index():
    # """Render the main dashboard with the current LED state."""
    # test_receive_email()
    send_email_trigger(5)   
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
    if temperature is not None and humidity is not None:
        sensor.save_data(temperature, humidity)  # Save the data to JSON
        if temperature > 24:
            send_email_trigger(temperature)
        return jsonify({'temperature': temperature, 'humidity': humidity})
    else:
        return jsonify({'error': 'Failed to read data from DHT11 sensor.'}), 500

@app.route('/toggle_fan', methods=['POST'])
def toggle_fan():
    # """Toggle the LED state based on the request from the frontend."""
    global FAN_STATE  # Use the global variable to keep track of the LED state

    # Get the state from the JSON request
    data = request.get_json()
    print(data['state'])
    if data['state'] == 'OFF':
        #turn_on_fan()
        FAN_STATE = 'ON'
    else:
        #turn_off_fan()
        FAN_STATE = 'OFF'  # Update the state variable

    # Return the current LED state as JSON
    return jsonify({'fan_state': FAN_STATE})

@app.route('/return_status', methods=['GET'])
def return_status():
    global LED_STATE, FAN_STATE
    return jsonify({'led_state': LED_STATE, 'fan_state': FAN_STATE})

@app.route('/api/light_intensity', methods=['POST'])
def get_light_data():
    global LED_STATE  # Use the global variable to keep track of the LED state

    data = request.json
    light_intensity = data.get('light_intensity')    
    print(data)
    print(light_intensity)
    if light_intensity < 1500:
        GPIO.output(led_pin, GPIO.HIGH)  # Turn the LED on
        LED_STATE = 'ON'  # Update the state variable
        send_email_notification('santisinsight@gmail.com')
    else:
        GPIO.output(led_pin, GPIO.LOW)  # Turn the LED on
        LED_STATE = 'OFF'  # Update the state variable

    return jsonify({'message': 'Data received successfully'})

def send_email_trigger(temperature):
    global email_thread_running
    recipient = 'santisinsight@gmail.com'

    # Run send_email in a separate thread
    email_thread = Thread(target=send_email, args=(recipient, temperature))
    email_thread.start()

    if not email_thread_running:
        email_thread_running = True
        threading.Thread(target=check_email_response).start()


def check_email_response():
    global email_thread_running
    count = 0
    try:
        while count < 5:
            count += 1
            # Check if a response has been received
            if receive_email():
                turn_on_fan()
                break  # Stop the loop once a valid response is received
            sleep(5)  # Wait before checking again
    finally:
        email_thread_running = False  # Reset the flag when done

# Replace with your Raspberry Pi's IP address if necessary
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000, debug=True)  # Run the Flask application
    finally:
        GPIO.cleanup()  # Ensures cleanup when the app stops # Run the Flask application


