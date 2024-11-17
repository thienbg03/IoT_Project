#include <WiFi.h>
#include <PubSubClient.h>

const int photoResistorPin = 34;

// WiFi credentials
const char* ssid = "GarciaPardo";
const char* password = "melbayjulian1";
//const char* ssid = "TP-Link_2AD8";
//const char* password = "14730078";

// MQTT Broker IP address 192.168.0.25
const char* mqtt_server = "192.168.0.25";
//const char* mqtt_server = "192.168.0.141";

// Initialize WiFi and MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
int value = 0;

// Flag to control publishing
bool stopPublishing = false;

// Timer variables
unsigned long previousMillis = 0;
const long interval = 3000; // 30 seconds

// Forward declaration
void callback(String topic, byte* message, unsigned int length);

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
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
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("vanieriot")) {
      Serial.println("connected");
      client.subscribe("room/control"); // Subscribe to control topic
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

  // Check if 30 seconds have passed
  unsigned long currentMillis = millis();
  if (!stopPublishing && currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    int value = analogRead(photoResistorPin);
    Serial.println("Analog value: ");
    Serial.println(value);

    // Convert the value to a JSON formatted string
    char message[50];
    sprintf(message, "{\"light_intensity\": %d}", value);
    
    // Publish the JSON value to the topic "light/intensity"
    client.publish("light/intensity", message);
    Serial.print("Published to light/intensity: ");
    Serial.println(message);
  }
}
