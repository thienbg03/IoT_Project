import json
import time

# Handle saving data to a .json file by replacing the old file
def save_data(temp, hum):
    data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temp,
        "humidity": hum
    }

    with open('../static/sensor_data.json', 'w+') as f:  
        f.seek(0)      
        f.truncate()   
        json.dump(data, f, indent=4)  

    print("Data saved:", data)