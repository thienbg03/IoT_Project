import paho.mqtt.client as mqtt
from email_notifier import send_email_notification  # Import the function

# Define the MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("light/intensity")

def on_message(client, userdata, msg):
    try:
        light_intensity = int(msg.payload.decode())
        print(f"Received light intensity: {light_intensity}")
        
        # Check if light intensity is below threshold
        if light_intensity < 400:
            send_email_notification()  # Call the imported email function
    except ValueError:
        print("Received non-integer message")

# Set up the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_start()
