
import os


class Config:
    # Configure your database URI (e.g., SQLite, PostgreSQL, MySQL)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    MAIL_SERVER=os.getenv('MAIL_SERVER')
    MAIL_PORT=os.getenv('MAIL_PORT')
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS')
    MAIL_USE_SSL=os.getenv('MAIL_USE_SSL')
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    SECRET_KEY=os.getenv('SECRET_KEY')
    
