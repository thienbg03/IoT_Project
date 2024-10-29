from .Freenove_DHT11 import DHT
import RPi.GPIO as GPIO
import time
import json

DHTPin = 18  # Define the pin of DHT11

class DHT11Sensor:
    def __init__(self, pin):
        self.dht = DHT.DHT(pin)
    
    def read_data(self):
        for i in range(15):  # Try reading up to 15 times to ensure data is correct
            chk = self.dht.readDHT11()
            if chk == self.dht.DHTLIB_OK:
                return self.dht.temperature, self.dht.humidity
            time.sleep(0.1)
        return None, None  # Return None if no valid reading

    def save_data(self, temp, hum):
        data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": temp,
            "humidity": hum
        }

        with open('sensor_data.json', 'w+') as f:  
            f.seek(0)      
            f.truncate()   
            json.dump(data, f, indent=4)  

        print("Data saved:", data)

if __name__ == '__main__':
    sensor = DHT11Sensor(DHTPin)
    try:
        while True:
            temperature, humidity = sensor.read_data()
            if temperature is not None and humidity is not None:
                sensor.save_data(temperature, humidity)
            else:
                print("Failed to read data from DHT11 sensor.")
            time.sleep(2)
    except KeyboardInterrupt:
        GPIO.cleanup()
