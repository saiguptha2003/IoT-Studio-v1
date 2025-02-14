from flask import Blueprint, jsonify
import paho.mqtt.client as mqtt
import threading
import time
from utils import token_required, cdb,getUniqueIDInt
from datetime import datetime

SelfHostBP = Blueprint('SelfHostBP', __name__)

# Global variable to store broker status
broker_status = {
    "status": "unknown",
    "last_check": None,
    "port": 1883,
    "host": "mqtt-broker"
}

def check_broker_status():
    try:
        client = mqtt.Client(client_id="status_checker", protocol=mqtt.MQTTv311, callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
        client.connect(broker_status["host"], broker_status["port"], keepalive=2)
        client.disconnect()
        return {
            "status": "running",
            "last_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "host": broker_status["host"],
            "port": broker_status["port"]
        }
    except Exception as e:
        return {
            "status": f"not running: {str(e)}",
            "last_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "host": broker_status["host"],
            "port": broker_status["port"]
        }

def CheckMQTTConnection():
    while True:
        try:
            broker_status.update(check_broker_status())
        except Exception as e:
            broker_status["status"] = f"not running: {str(e)}"
        
        broker_status["last_check"] = time.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(30)  # Check every 30 seconds

status_thread = threading.Thread(target=CheckMQTTConnection, daemon=True)
status_thread.start()
@SelfHostBP.route('/mqtt/status', methods=['GET'])
@token_required
def get_mqtt_status(userid, email, username):
    try:
        return jsonify({
            "broker": {
                "status": broker_status["status"],
                "last_checked": broker_status["last_check"],
                "host": broker_status["host"],
                "ports": {
                    "mqtt": broker_status["port"],
                    "websocket": 9001
                }
            }
        }), 200
    except Exception as e:
        return jsonify({
            "error": f"Failed to get broker status: {str(e)}"
        }), 500 