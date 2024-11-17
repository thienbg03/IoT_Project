const int photoResistorPin = 34;
const int ledPin = 26;
int lightThreshold = 400;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int value = analogRead(photoResistorPin);
  Serial.println("Analog value: ");
  Serial.println(value);

  if (value < lightThreshold)
  {
    digitalWrite(ledPin, HIGH);
  }
  else
  {
    digitalWrite(ledPin, LOW);
  }
  delay(1000);
}
