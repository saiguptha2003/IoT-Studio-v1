import json
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify,request
from models import db
from Config import Config
from routes import authBP, IoTConnectBP,SecureStoreBP,BasicBP,TriggerBP,WareHouseBP,SelfHostBP
from flask_cors import CORS
import os
from cache import redisClient
import couchdb
load_dotenv()
FLASK_PORT=os.getenv('FLASK_PORT')
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
logging.basicConfig(level=logging.DEBUG)

CORS(app, resources={
    r"/services/WareHouse/*": {
        "origins": "http://localhost:5173",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

app.register_blueprint(authBP, url_prefix='/auth')
app.register_blueprint(IoTConnectBP, url_prefix='/services/IotConnect')
app.register_blueprint(SecureStoreBP, url_prefix='/services/SecureStore')
app.register_blueprint(WareHouseBP,url_prefix="/services/WareHouse")
app.register_blueprint(BasicBP,url_prefix='/')
app.register_blueprint(TriggerBP,url_prefix='/Trigger')
app.register_blueprint(SelfHostBP, url_prefix="/services/SelfHost")
@app.route("/",methods=["GET"])
def index():
    return {"message": "hello User.."}
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.route("/contact-us",methods=["GET"])
def contactUs():
    return {"Name": "V D Panduranga Sai Guptha", "Email":"saiguptha_v@srmap.edu.in"}


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {"error": "No file part"}, 400

    file = request.files['file']

    if file.filename == '':
        return {"error": "No selected file"}, 400

    # Read first 5 lines
    first_5_lines = []
    for i, line in enumerate(file.stream):
        if i >= 5:
            break
        first_5_lines.append(line.decode('utf-8').strip())
    logging.info(file.filename)

    return {
        "filename": file.filename,
        "first_5_lines": first_5_lines
    }



@app.route('/get/<key>', methods=['GET'])
def get_data(key):
    try:
        # Get value from Redis
        value = redisClient.get(key)
        if value is None:
            return jsonify({"error": "Key not found"}), 404
        return json.loads(value), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import sys
    testing = "--test" in sys.argv
    if testing:
        print("Running in test mode")
    else:
        app.run(host="0.0.0.0", port=5000, debug=True)
