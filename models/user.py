from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # Optional: explicit table name
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    rfid_id = db.Column(db.String(20), unique=True, nullable=False)
    temperature_threshold = db.Column(db.Float, nullable=False, default=24.0)
    light_intensity_threshold = db.Column(db.Float, nullable=False, default=1500.0)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} | RFID: {self.rfid_id}>"
