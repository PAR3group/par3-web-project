from par3 import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    phonenumber = db.Column(db.String(20), unique=True, nullable=False)
    birthdate = db.Column(db.Date(), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False)