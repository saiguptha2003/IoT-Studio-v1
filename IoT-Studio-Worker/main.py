from concurrent.futures import ThreadPoolExecutor
import time
from flask import Flask, jsonify, request, send_file
import paho.mqtt.client as mqtt
import openpyxl
import logging
import threading
import sqlite3
import json
import os
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

DATABASE = 'connections.db'

# Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connections (
            trigger_id TEXT,
            user_id TEXT,
            status TEXT,
            connection_id TEXT,
            created_at TEXT,
            closed_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize global user connections
user_connections = {}

# MQTT connection callback functions
def on_connect(client, userdata, flags, rc, properties=None):
    logging.info(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(userdata['subscribe_topic'], qos=userdata['qos'])

def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        message = json.loads(msg.payload.decode("utf-8"))
        if isinstance(message, dict):
            user_id = userdata['user_id']
            trigger_id = userdata['trigger_id']
            connection_id = userdata['connection_id']
            excel_filename = f"{user_id}_{trigger_id}_{connection_id}.xlsx"
            if os.path.exists(excel_filename):
                wb = openpyxl.load_workbook(excel_filename)
                ws = wb.active
            else:
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.append(["Timestamp"] + list(message.keys()))
            row_data = [timestamp] + list(message.values())
            ws.append(row_data)
            wb.save(excel_filename)
        else:
            logging.error("Received message is not a valid JSON object.")
    except json.JSONDecodeError:
        logging.error("Failed to decode message as JSON.")
    except Exception as e:
        logging.error(f"Error handling message: {e}")

# MQTT connection handling in a separate thread
def mqtt_connection_thread(user_data):
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.user_data_set(user_data)

    # Connect to the MQTT broker
    mqtt_client.connect(user_data['connection_url'], user_data['port'], user_data['keep_alive'])
    mqtt_client.loop_start()

    # Track the connection
    user_connections[user_data['user_id'] + "_" + user_data['trigger_id']] = mqtt_client

    # Insert connection information into the database
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO connections (trigger_id, user_id, status, connection_id, created_at, closed_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_data['trigger_id'], user_data['user_id'], 'running', user_data['connection_id'], created_at, None))
    conn.commit()
    conn.close()
    logging.info(f"MQTT connection started for {user_data['user_id']} with trigger {user_data['trigger_id']}.")

# Start MQTT connection through API endpoint
@app.route('/start_connection', methods=['POST'])
def start_connection():
    try:
        user_data = request.get_json()

        # Extract connection details
        connection_details = user_data.get("connection_details")
        if not connection_details:
            logging.info("No connection details")
            return jsonify({"error": "connection_details are required"}), 400

        user_id = user_data.get("user_id")
        trigger_id = user_data.get("trigger_id")
        if not user_id or not trigger_id:
            logging.info("user data not avaiable")
            return jsonify({"error": "user_id and trigger_id are required"}), 400

        # Prepare the userdata dictionary
        mqtt_userdata = {
            "user_id": user_id,
            "trigger_id": trigger_id,
            "connection_id": connection_details.get("connection_id"),
            "connection_url": connection_details.get("connection_url"),
            "port": connection_details.get("port", 1883),
            "qos": connection_details.get("qos", 0),
            "keep_alive": connection_details.get("keep_alive", 60),
            "subscribe_topic": connection_details.get("subscribe_topic")
        }

        # Start the MQTT connection in a separate thread
        connection_thread = threading.Thread(target=mqtt_connection_thread, args=(mqtt_userdata,))
        connection_thread.start()

        return jsonify({"status": "Connection started", "user_id": user_id, "trigger_id": trigger_id})

    except Exception as e:
        logging.error(f"Error starting connection: {e}")
        return jsonify({"error": "Failed to start connection"}), 500

# Stop MQTT connection through API endpoint
@app.route('/stop_connection', methods=['POST'])
def stop_connection():
    try:
        stop_data = request.json
        user_id = stop_data.get("user_id")
        trigger_id = stop_data.get("trigger_id")
        connection_id = stop_data.get("connection_id")

        if not user_id or not trigger_id:
            return jsonify({"error": "user_id and trigger_id are required to stop"}), 400

        connection_key = f"{user_id}_{trigger_id}"
        if connection_key in user_connections:
            mqtt_client = user_connections.pop(connection_key)
            mqtt_client.loop_stop()
            mqtt_client.disconnect()

            logging.info(f"Connection stopped for {user_id} with trigger {trigger_id}.")

            # Update database with connection status as 'ended'
            closed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE connections
                SET status = ?, closed_at = ?
                WHERE trigger_id = ? AND user_id = ? AND connection_id = ?
            ''', ('ended', closed_at, trigger_id, user_id, connection_id))
            conn.commit()
            conn.close()

            # Send the Excel file if it exists
            excel_filename = f"{user_id}_{trigger_id}_{connection_id}.xlsx"
            if os.path.exists(excel_filename):
                response = send_file(excel_filename, download_name=excel_filename, as_attachment=True)
                return response
            else:
                logging.error(f"Excel file not found: {excel_filename}")
                return jsonify({"error": "Excel file not found"}), 404
        else:
            return jsonify({"error": "Connection not found for the given user_id and trigger_id"}), 404
    except Exception as e:
        logging.error(f"Error stopping connection: {e}")
        return jsonify({"error": "Failed to stop connection"}), 500

# Fetch connection status through API endpoint
@app.route('/connection_status', methods=['POST'])
def connection_status():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request payload must be JSON"}), 400

        user_id = data.get('user_id')
        trigger_id = data.get('trigger_id')
        connection_id = data.get('connection_id')  # Optional

        if not user_id or not trigger_id:
            return jsonify({"error": "user_id and trigger_id are required"}), 400

        # Query the database for the connection status
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            if connection_id:
                cursor.execute('''
                    SELECT status, created_at, closed_at
                    FROM connections
                    WHERE user_id = ? AND trigger_id = ? AND connection_id = ?
                ''', (user_id, trigger_id, connection_id))
            else:
                cursor.execute('''
                    SELECT status, created_at, closed_at
                    FROM connections
                    WHERE user_id = ? AND trigger_id = ?
                ''', (user_id, trigger_id))

            records = cursor.fetchall()

        if not records:
            return jsonify({"error": "No connection found for the given parameters"}), 404

        response = [{"status": status, "created_at": created_at, "closed_at": closed_at} for status, created_at, closed_at in records]

        return jsonify({"connections": response}), 200

    except Exception as e:
        logging.error(f"Error fetching connection status: {e}")
        return jsonify({"error": "Failed to retrieve connection status"}), 500

# Cleanup function to remove ended connections and their associated files
def cleanup_ended_records():
    while True:
        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT user_id, trigger_id, connection_id FROM connections WHERE status = 'ended'")
                ended_records = cursor.fetchall()

                for user_id, trigger_id, connection_id in ended_records:
                    excel_filename = f"{user_id}_{trigger_id}_{connection_id}.xlsx"

                    if os.path.exists(excel_filename):
                        os.remove(excel_filename)
                        logging.info(f"Removed Excel file: {excel_filename}")
                    else:
                        logging.warning(f"Excel file not found: {excel_filename}")

                cursor.execute("DELETE FROM connections WHERE status = 'ended'")
                conn.commit()
                logging.info("Deleted records with status 'ended' from the database.")
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")
        
        time.sleep(100)

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_ended_records, daemon=True)
cleanup_thread.start()

# Run the Flask application
if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=4)
    init_db()
    app.run(host="0.0.0.0", port=4342, threaded=True)
