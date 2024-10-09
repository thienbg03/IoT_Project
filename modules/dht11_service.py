import json
import time

# handle saving data to a .json file so that it can be used for data presentation
def save_data(temp, hum):
    data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temp,
        "humidity": hum
    }
    with open('sensor_data.json', 'a') as f:
        f.write(json.dumps(data) + '\n')
    print("Data saved:", data)
