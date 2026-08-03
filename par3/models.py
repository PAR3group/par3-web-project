from par3 import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    phonenumber = db.Column(db.String(20), unique=True, nullable=False)
    user_sex = db.Column(db.String(10), nullable=False)
    experience_years = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)