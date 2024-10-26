from flask import Blueprint, request, jsonify
from modules.dht11_service import save_data

dht11_blueprint = Blueprint('dht11', __name__)

@dht11_blueprint.route('/submit_data', methods=['POST'])
def submit_data():
    data = request.json
    temp = data.get('temperature')
    hum = data.get('humidity')

    if temp is None or hum is None:
        return jsonify({"error": "Invalid data format"}), 400

    save_data(temp, hum)  # Save the data using the service
    return jsonify({"message": "Data received successfully"}), 200
