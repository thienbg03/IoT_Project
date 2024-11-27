from app import app, db
from models.user import User

# Predefined users to populate the database
users = [
    {
        "first_name": "Alice",
        "last_name": "Smith",
        "rfid_id": "111111",
        "temperature_threshold": 24.0,
        "light_intensity_threshold": 1000.0
    },
    {
        "first_name": "Bob",
        "last_name": "Johnson",
        "rfid_id": "222222",
        "temperature_threshold": 28.0,
        "light_intensity_threshold": 1200.0
    },
    {
        "first_name": "Charlie",
        "last_name": "Brown",
        "rfid_id": "333333",
        "temperature_threshold": 30.0,
        "light_intensity_threshold": 1500.0
    }
]

with app.app_context():
    db.create_all()  # Ensure the database is created

    for user_data in users:
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            rfid_id=user_data['rfid_id'],
            temperature_threshold=user_data['temperature_threshold'],
            light_intensity_threshold=user_data['light_intensity_threshold']
        )
        db.session.add(user)

    db.session.commit()
    print("Database populated with test users.")
