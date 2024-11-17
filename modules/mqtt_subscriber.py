import paho.mqtt.client as mqtt
from email_notifier import send_email_notification  # Import the email function

# Define the MQTT callback functions
def on_connect(client, userdata, flags, reason_code, properties=None):
    """Handle connection to MQTT broker."""
    print(f"Connected with reason code: {reason_code}")
    client.subscribe("light/intensity")  # Subscribe to the topic

def on_message(client, userdata, msg):
    """Handle incoming MQTT messages."""
    try:
        light_intensity = int(msg.payload.decode())  # Decode the message
        print(f"Received light intensity: {light_intensity}")
        
        # Trigger email if light intensity is below the threshold
        if light_intensity < 400:
            send_email_notification()
    except ValueError:
        print("Received non-integer message")

# Set up the MQTT client with MQTTv5 protocol
client = mqtt.Client(protocol=mqtt.MQTTv5)  # Explicitly use MQTT version 5
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker and start the loop
client.connect("localhost", 1883, 60)  # Ensure the broker is running on localhost
client.loop_start()

# Keep the script running
try:
    while True:
        pass  # Prevent script termination
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("Disconnected from MQTT broker.")
