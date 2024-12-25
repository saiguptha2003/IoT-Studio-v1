import openpyxl
import paho.mqtt.client as mqtt
import logging
from datetime import datetime
from threading import Thread

# Setting up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MQTTSensorClient:
    def __init__(self, user_id, trigger_id, connection_id, connection_url, port, subscribe_topic, qos, keep_alive):
        self.user_id = user_id
        self.trigger_id = trigger_id
        self.connection_id = connection_id
        self.connection_url = connection_url
        self.port = port
        self.subscribe_topic = subscribe_topic
        self.qos = qos
        self.keep_alive = keep_alive
        self.active = False
        self.file_name = f"{self.user_id}_{self.trigger_id}_{self.connection_id}.xlsx"

        # Initialize MQTT client
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Create an Excel file and write headers
        self.create_excel_file()

    def create_excel_file(self):
        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(["Timestamp", "Topic", "Message"])
            workbook.save(self.file_name)
            logger.info(f"[{self.connection_id}] Excel file created: {self.file_name}")
        except Exception as e:
            logger.error(f"[{self.connection_id}] Failed to create Excel file: {e}")

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            logger.info(f"[{self.connection_id}] Connected to MQTT broker with result code {rc}")
            self.active = True
            client.subscribe(self.subscribe_topic, qos=self.qos)
        else:
            logger.error(f"[{self.connection_id}] Connection failed with result code {rc}")

    def on_message(self, client, userdata, msg):
        logger.info(f"[{self.connection_id}] Received on {msg.topic}: {msg.payload.decode()}")
        if self.active:
            # Verify the data is passed correctly before writing
            logger.debug(f"[{self.connection_id}] Processing data for topic {msg.topic} with message: {msg.payload.decode()}")
            self.write_to_excel(msg.topic, msg.payload.decode())
        else:
            logger.warning(f"[{self.connection_id}] Subscriber is inactive, message ignored")

    def write_to_excel(self, topic, message):
        try:
            workbook = openpyxl.load_workbook(self.file_name)
            sheet = workbook.active
            # Log data that will be written to the Excel file
            logger.info(f"[{self.connection_id}] Writing to Excel: Timestamp={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, Topic={topic}, Message={message}")
            sheet.append([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), topic, message])
            workbook.save(self.file_name)
            logger.info(f"[{self.connection_id}] Message successfully logged to Excel: {message}")
        except Exception as e:
            logger.error(f"[{self.connection_id}] Failed to write to Excel: {e}")

    def start_connection(self):
        try:
            logger.info(f"[{self.connection_id}] Connecting to broker at {self.connection_url}:{self.port}...")
            self.client.connect(self.connection_url, self.port, self.keep_alive)
            logger.info(f"[{self.connection_id}] Connected to MQTT broker.")
            self.client.loop_start()  # Start MQTT loop in a separate thread
        except Exception as e:
            logger.error(f"[{self.connection_id}] Connection failed: {e}")

    def stop_connection(self):
        self.client.disconnect()
        self.client.loop_stop()
        logger.info(f"[{self.connection_id}] Connection stopped.")

def start_connection_handler(user_id, trigger_id, connection_id, connection_url, port, subscribe_topic, qos, keep_alive):
    client = MQTTSensorClient(user_id, trigger_id, connection_id, connection_url, port, subscribe_topic, qos, keep_alive)
    client.start_connection()
    return client

def stop_connection_handler(client):
    client.stop_connection()


# Code to run when the script is executed
print("Config script is running")

# Example usage with POST data simulation
user_id = "user123"
trigger_id = "trigger001"
connection_id = "connectdion_001"
connection_url = "broker.emqx.io"
port = 1883
subscribe_topic = "paho/test/topic"
qos = 2
keep_alive = 60

# Start the connection in a new thread (simulating POST request for starting)
client = start_connection_handler(user_id, trigger_id, connection_id, connection_url, port, subscribe_topic, qos, keep_alive)

# Simulate stopping the connection (after some time, e.g., 10 seconds)
# This is where you'd call stop_connection_handler(client) from an endpoint or event trigger
# For demonstration, stopping after 10 seconds.
import time
time.sleep(100)
stop_connection_handler(client)
