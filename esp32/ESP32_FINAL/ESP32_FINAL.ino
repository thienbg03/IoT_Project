#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <PubSubClient.h>

#define SS_PIN 5  // SDA Pin on RC522
#define RST_PIN 4 // RST Pin on RC522
#define PHOTO_RESISTOR_PIN 34

// WiFi credentials
const char* ssid = "Ruri";
//const char* ssid = "TP-Link_2AD8";
const char* password = "12345678";
//const char* password = "14730078";

// MQTT Broker IP address
const char* mqtt_server = "192.168.29.33";
//const char* mqtt_server = "192.168.29.208";
const char* mqtt_server = "192.168.29.214";
//const char* mqtt_server = "192.168.0.141";
//const char* mqtt_server = "192.168.0.129";
// Initialize WiFi and MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);

MFRC522 rfid(SS_PIN, RST_PIN);

unsigned long previousLightMillis = 0;
const long lightInterval = 3000; // 3 seconds

bool stopPublishing = false;

void setup() {
  Serial.begin(115200);

  // Setup WiFi and MQTT
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // Setup RFID
  SPI.begin(18, 19, 23, SS_PIN);
  rfid.PCD_Init();
  Serial.println("Place your RFID card near the reader...");
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
  Serial.println(topic);

  String messagein;
  for (int i = 0; i < length; i++) {
    messagein += (char)message[i];
  }

  if (topic == "room/control") {
    if (messagein == "STOP") {
      stopPublishing = true;
      Serial.println("Publishing stopped");
    } else if (messagein == "START") {
      stopPublishing = false;
      Serial.println("Publishing resumed");
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection... ");
    String clientId = "ESP32Client-" + String(WiFi.macAddress());
    if (client.connect(clientId.c_str())) {
      Serial.println("Connected to MQTT broker");
      client.subscribe("room/control");
    } else {
      Serial.print("Connection failed, rc=");
      Serial.print(client.state());
      Serial.println(" - retrying in 5 seconds");
      delay(5000);
    }
  }
}

void publishLightIntensity() {
  int value = analogRead(PHOTO_RESISTOR_PIN);
  char message[50];
  sprintf(message, "{\"light_intensity\": %d}", value);
  client.publish("light/intensity", message);
  Serial.print("Published to light/intensity: ");
  Serial.println(message);
}

void checkRFID() {
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
    return;
  }

  char uidMessage[50];
  sprintf(uidMessage, "{\"rfid_code\": \"");
  for (byte i = 0; i < rfid.uid.size; i++) {
    char hexByte[4];
    sprintf(hexByte, "%02X", rfid.uid.uidByte[i]);
    strcat(uidMessage, hexByte);
  }
  strcat(uidMessage, "\"}");
  client.publish("rfid/code", uidMessage);
  Serial.print("Published to rfid/code: ");
  Serial.println(uidMessage);

  rfid.PICC_HaltA();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long currentMillis = millis();
  if (!stopPublishing && currentMillis - previousLightMillis >= lightInterval) {
    previousLightMillis = currentMillis;
    publishLightIntensity();
  }

  checkRFID();
}
