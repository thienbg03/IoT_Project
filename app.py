from flask import Flask, render_template, request, jsonify
from models.user import db, User  # Import the database and User model
import RPi.GPIO as GPIO
from routes.dht11_routes import dht11_blueprint
from modules.fan import turn_on_fan, turn_off_fan
import threading
from modules.DHT11 import DHT11Sensor  # Import the updated DHT11Sensor class
from time import sleep
from modules.email_handler import send_temperature_email, send_light_email, send_login_email, receive_email # Import the send_temperature_email function
from threading import Thread
# from modules.mqtt_subscriber import email_notifier
from modules.bluetooth_scanner import scan_bluetooth_devices, get_bluetooth_data

# Initialize the Flask application
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# simulation with fake data to see if the saving works:
# app.register_blueprint(dht11_blueprint)
# Set up GPIO
led_pin = 16  # Define the GPIO pin number for the LED
DHT_PIN = 18

# Initial LED statesudo apt-get install python3-rpi.gpio
sensor = DHT11Sensor(DHT_PIN)

# Start with the LED turned off
# Initialize global states
LED_STATE = 'OFF'
FAN_STATE = 'OFF'
LIGHT_INTENSITY = 0
EMAIL_STATUS = "UNSENT"
USER_TAG = 'default'
email_thread_running = False

def setup_gpio_and_db():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_pin, GPIO.OUT)
    with app.app_context():
        db.create_all()  # Creates the database tables

# Call the function explicitly before running the app
setup_gpio_and_db()

@app.route('/')
def index():
     # Set the pin as an output
    GPIO.output(led_pin, GPIO.LOW)
    send_email_trigger(5)
    return render_template('index.html', led_state=LED_STATE)


@app.route('/toggle_led', methods=['POST'])
def toggle_led():
    # """Toggle the LED state based on the request from the frontend."""
    global LED_STATE  # Use the global variable to keep track of the LED state
    # Get the state from the JSON request
    data = request.get_json()
    #print(data['state'])
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

@app.route('/bluetooth/devices', methods=['GET'])
def get_bluetooth_devices():
    devices = scan_bluetooth_devices()
    # save_devices_to_json(devices)
    return jsonify(devices)

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
    global FAN_STATE, EMAIL_STATUS  # Use the global variable to keep track of the LED state

    # Get the state from the JSON request
    data = request.get_json()
    #print(data['state'])
    if data['state'] == 'OFF':
        turn_on_fan()
        FAN_STATE = 'ON'
    else:
        EMAIL_STATUS = "UNSENT"
        turn_off_fan()
        FAN_STATE = 'OFF'  # Update the state variable

    # Return the current LED state as JSON
    return jsonify({'fan_state': FAN_STATE})

@app.route('/return_status', methods=['GET'])
def return_status():
    global LED_STATE, FAN_STATE, EMAIL_STATUS, LIGHT_INTENSITY
    return jsonify({'led_state': LED_STATE, 'fan_state': FAN_STATE, 'email_status': EMAIL_STATUS, 'light_intensity': LIGHT_INTENSITY})

@app.route('/api/light_intensity', methods=['POST'])
def get_light_data():
    global LED_STATE, EMAIL_STATUS, LIGHT_INTENSITY  # Use the global variable to keep track of the LED state
    data = request.json
    LIGHT_INTENSITY = data.get('light_intensity')
    #print(data)
    #print(LIGHT_INTENSITY)
    
    if LIGHT_INTENSITY is None:
        return jsonify({'error': 'light_intensity is required and cannot be None'}), 400
    
    if LIGHT_INTENSITY < 0:
        GPIO.output(led_pin, GPIO.HIGH)  # Turn the LED on
        LED_STATE = 'ON'  # Update the state variable
        EMAIL_STATUS = "SENT"
        send_light_email('cevelinevangelista@gmail.com')
    else:
        GPIO.output(led_pin, GPIO.LOW)  # Turn the LED off
        EMAIL_STATUS = "UNSENT"
        LED_STATE = 'OFF'  # Update the state variable

    return jsonify({'message': 'Data received successfully', 'light_intensity': LIGHT_INTENSITY})

@app.route('/api/rfid', methods=['POST'])
def get_rfid_data():
    global LED_STATE, EMAIL_STATUS, LIGHT_INTENSITY  # Use the global variable to keep track of the LED state
    data = request.json
    if not data or "rfid_code" not in data:
        return jsonify({"error": "Invalid request, missing 'rfid_code'"}), 400
    
    # Get the RFID code from the request
    USER_TAG = data.get("rfid_code")
    print(data)
    print(USER_TAG)
    
    email_thread = Thread(target=send_login_email, args=('santisinsight@gmail.com', USER_TAG))
    email_thread.start()

    return jsonify({'message': 'Data received successfully', 'light_intensity': LIGHT_INTENSITY})


@app.route('/get_light_data', methods=['GET'])
def send_light_data():
    # Simulating light intensity data for testing purposes
    global LIGHT_INTENSITY
    return jsonify({'light_intensity': LIGHT_INTENSITY})

def send_email_trigger(temperature):
    global email_thread_running
    recipient = 'santisinsight@gmail.com'

    # Run send_temperature_email in a separate thread
    email_thread = Thread(target=send_temperature_email, args=(recipient, temperature))
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

@app.route('/add_user', methods=['POST'])
def add_user():
    """Add a new user to the database."""
    try:
        data = request.get_json()
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            rfid_id=data['rfid_id'],
            temperature_threshold=data['temperature_threshold'],
            light_intensity_threshold=data['light_intensity_threshold']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully!'})
    except Exception as e:
        db.session.rollback()  # Rollback in case of failure
        return jsonify({'error': f'Failed to add user: {str(e)}'}), 500


@app.route('/users', methods=['GET'])
def get_users():
    """Retrieve all users."""
    users = User.query.all()
    return jsonify([
        {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'rfid_id': user.rfid_id,
            'temperature_threshold': user.temperature_threshold,
            'light_intensity_threshold': user.light_intensity_threshold
        }
        for user in users
    ])

@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update thresholds for a specific user."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    user.temperature_threshold = data.get('temperature_threshold', user.temperature_threshold)
    user.light_intensity_threshold = data.get('light_intensity_threshold', user.light_intensity_threshold)
    db.session.commit()
    return jsonify({'message': 'User thresholds updated successfully!'})

# This route assigns a tag to a user:
@app.route('/assign_rfid', methods=['POST'])
def assign_rfid():
    """Assign an RFID tag to a user."""
    data = request.get_json()
    rfid_id = data.get('rfid_id')
    user_id = data.get('user_id')

    if not rfid_id or not user_id:
        return jsonify({'error': 'RFID and User ID are required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Assign the RFID tag
    user.rfid_id = rfid_id
    db.session.commit()
    return jsonify({'message': f'RFID tag {rfid_id} assigned to {user.first_name} {user.last_name}.'})

# This route reads an RFID tag, verifies its validity, and returns the user's thresholds:
@app.route('/read_rfid', methods=['POST'])
def read_rfid():
    """Read an RFID tag and return the user's profile."""
    data = request.get_json()
    rfid_id = data.get('rfid_id')

    if not rfid_id:
        return jsonify({'error': 'RFID is required'}), 400

    # Find the user with the given RFID
    user = User.query.filter_by(rfid_id=rfid_id).first()
    if not user:
        return jsonify({'error': 'Invalid RFID tag'}), 404

    # Return the user's profile and thresholds
    return jsonify({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'rfid_id': user.rfid_id,
        'temperature_threshold': user.temperature_threshold,
        'light_intensity_threshold': user.light_intensity_threshold
    })

# This route updates the temperature or light intensity thresholds:
@app.route('/update_thresholds', methods=['POST'])
def update_thresholds():
    """Update the temperature and light intensity thresholds for a user."""
    data = request.get_json()
    rfid_id = data.get('rfid_id')

    if not rfid_id:
        return jsonify({'error': 'RFID is required'}), 400

    user = User.query.filter_by(rfid_id=rfid_id).first()
    if not user:
        return jsonify({'error': 'Invalid RFID tag'}), 404

    # Update the thresholds
    user.temperature_threshold = data.get('temperature_threshold', user.temperature_threshold)
    user.light_intensity_threshold = data.get('light_intensity_threshold', user.light_intensity_threshold)
    db.session.commit()

    return jsonify({'message': 'Thresholds updated successfully!'})

# Replace with your Raspberry Pi's IP address if necessary
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000, debug=True)  # Run the Flask application
    finally:
        GPIO.cleanup()  # Ensures cleanup when the app stops # Run the Flask application
