import ctypes
import os

class DHT:
    DHTLIB_OK = 0  # Define the return code for a successful read

    def __init__(self, pin):
        # Load the shared library
        lib_path = os.path.join(os.path.dirname(__file__), 'libdht.so')
        self.lib = ctypes.CDLL(lib_path)
        
        # Set up the DHT11 pin
        self.lib.setDHT11Pin.argtypes = [ctypes.c_int]
        self.lib.setDHT11Pin(pin)

        # Define the functions in libdht.so
        self.lib.readDHT11.restype = ctypes.c_int
        self.lib.getHumidity.restype = ctypes.c_double
        self.lib.getTemperature.restype = ctypes.c_double

        # Initialize humidity and temperature attributes
        self.humidity = 0.0
        self.temperature = 0.0

    def readDHT11(self):
        # Call the read function
        result = self.lib.readDHT11()
        if result == self.DHTLIB_OK:
            # If successful, retrieve humidity and temperature
            self.humidity = self.lib.getHumidity()
            self.temperature = self.lib.getTemperature()
        return result
