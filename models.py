from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) #an id for every user, primary key
    username = db.Column(db.String(80), unique=True, nullable=False) #a unique username for users
    password_hash = db.Column(db.String(200), nullable=False) #only the hash of the password is stored
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) #timestamp of the account creation to log weight and height during account completion
