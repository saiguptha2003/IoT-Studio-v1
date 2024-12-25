from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Trigger(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.String(120), nullable=False)
    trigger_id=db.Column(db.String(120), nullable=False)
    create_at=db.Column(db.DateTime)
    status=db.Column(db.String)