#include <WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "TP-Link_2AD8";
const char* password = "14730078";

// MQTT Broker IP address
const char* mqtt_server = "192.168.0.141";

// Initialize WiFi and MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

// LED Pin
const int ledPin = 26;

// Flag to control publishing
bool stopPublishing = false;

// Forward declaration
void callback(String topic, byte* message, unsigned int length);

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // Ensure the LED is initially off
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  
  String messagein;
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messagein += (char)message[i];
  }
  Serial.println();

  // Check for the control topic
  if (topic == "room/control") {
    if (messagein == "STOP") {
      stopPublishing = true; // Stop publishing
      Serial.println("Publishing stopped");
    } else if (messagein == "START") {
      stopPublishing = false; // Resume publishing
      Serial.println("Publishing resumed");
    }
  }

  // Control the LED based on a different topic
  if (topic == "room/light") {
    if (messagein == "ON") {
      digitalWrite(ledPin, HIGH); // Turn the LED on
      Serial.println("LED is ON");
    } else if (messagein == "OFF") {
      digitalWrite(ledPin, LOW); // Turn the LED off
      Serial.println("LED is OFF");
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("vanieriot")) {
      Serial.println("connected");
      client.subscribe("room/control"); // Subscribe to control topic
      client.subscribe("room/light");   // Subscribe to LED control topic
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Only publish if stopPublishing is false
  if (!stopPublishing) {
    client.publish("IoTlab/ESP32", "Hello, I'm ESP32");
    Serial.println("Published: Hello, I'm ESP32");
    delay(5000);
  }
}
