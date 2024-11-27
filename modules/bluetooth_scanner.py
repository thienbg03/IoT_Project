import os
import json
import time
from bluepy.btle import Scanner
from threading import Thread
from bluepy.btle import BTLEManagementError

# JSON file to store Bluetooth data
data_file = "bluetooth_data.json"
scan_interval = 10  # seconds

# Initialize the JSON file if it doesn't exist
if not os.path.exists(data_file):
    with open(data_file, 'w') as f:
        json.dump([], f)

def scan_bluetooth_devices():
    """Scan for Bluetooth devices and overwrite the JSON file with fresh data."""
    while True:
        try:
            # Initialize the Bluetooth scanner
            scanner = Scanner()
            devices = scanner.scan(5.0)  # Scan for 5 seconds
            bluetooth_data = []

            # Collect device information
            for device in devices:
                device_info = {
                    "address": device.addr,
                    "rssi": device.rssi,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                bluetooth_data.append(device_info)

            print(f"Scan complete: {len(bluetooth_data)} devices found.")
            return bluetooth_data
            # Overwrite the JSON file with the latest scan data
            # with open(data_file, 'w') as f:
            #     json.dump(bluetooth_data, f, indent=4)
            # 

        except BTLEManagementError as e:
            print(f"Bluetooth scan error: {e}")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

        # # Wait for the next scan interval
        # time.sleep(scan_interval)

# Function to get the scanned data
def get_bluetooth_data():
    """Load saved Bluetooth data from JSON."""
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return []
