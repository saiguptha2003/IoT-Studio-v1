from flask import Flask
from models import db
from Config import Config
from routes import authBP
from flask_cors import CORS
import couchdb
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

CORS(app)
from constants import DBNAME
couch = couchdb.Server('https://admin:iotstudio@couchdb-xfm8.onrender.com/')
DBNAME='iotstudio'

if DBNAME not in couch:
    cdb = couch.create(DBNAME)
else:
    cdb = couch[DBNAME]
    
app.register_blueprint(authBP, url_prefix='/auth')

@app.route("/",methods=["GET"])
def index():
    return {"message": "hello User.."}
if __name__ == "__main__":
    import sys
    testing = "--test" in sys.argv
    if testing:
        print("Running in test mode")
        # Perform any setup for test mode
    else:
        app.run(host="0.0.0.0", port=5000)
