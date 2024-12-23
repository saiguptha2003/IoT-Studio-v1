from flask import Flask
from models import db
from Config import Config
from routes import authBP, IoTConnectBP,SecureStoreBP,BasicBP
from flask_cors import CORS
import couchdb
from constants import DBNAME
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

CORS(app)
    
app.register_blueprint(authBP, url_prefix='/auth')
app.register_blueprint(IoTConnectBP, url_prefix='/services/IotConnect')
app.register_blueprint(SecureStoreBP, url_prefix='/services/SecureStore')
app.register_blueprint(BasicBP,url_prefix='/')

@app.route("/",methods=["GET"])
def index():
    return {"message": "hello User.."}
if __name__ == "__main__":
    import sys
    testing = "--test" in sys.argv
    if testing:
        print("Running in test mode")
    else:
        app.run(host="0.0.0.0", port=5000)
