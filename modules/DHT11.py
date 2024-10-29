from Freenove_DHT11 import DHT
import RPi.GPIO as GPIO
import time

DHTPin = 17  # Define the pin of DHT11

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

if __name__ == '__main__':
    sensor = DHT11Sensor(DHTPin)
    try:
        while True:
            temperature, humidity = sensor.read_data()
            print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
            time.sleep(2)
    except KeyboardInterrupt:
        GPIO.cleanup()
