
import os


class Config:
    # Configure your database URI (e.g., SQLite, PostgreSQL, MySQL)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY=os.getenv('SECRET_KEY')
    
