
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_name = db.Column(db.String(120),unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    uniqueID=db.Column(db.String(32),nullable=False,unique=True)
    
