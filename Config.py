
class Config:
    # Configure your database URI (e.g., SQLite, PostgreSQL, MySQL)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_USERNAME='adminIoTStudio@gmail.com'
    MAIL_PASSWORD='Pandusai@2003'
    SECRET_KEY="5zp\xdeD\xa3/)\xf1\x87\x80\xf5"
    
