import grpc
from concurrent import futures
import time
import iot_service_pb2
import iot_service_pb2_grpc
import paho.mqtt.client as mqtt
import openpyxl
import logging
import threading
import sqlite3
import json
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
DATABASE = 'connections.db'
user_connections = {}

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

# MQTT Handling
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
            ws.append([timestamp] + list(message.values()))
            wb.save(excel_filename)
    except Exception as e:
        logging.error(f"Error handling message: {e}")

def mqtt_connection_thread(user_data):
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.user_data_set(user_data)

    mqtt_client.connect(user_data['connection_url'], user_data['port'], user_data['keep_alive'])
    mqtt_client.loop_start()

    user_connections[user_data['user_id'] + "_" + user_data['trigger_id']] = mqtt_client

    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO connections (trigger_id, user_id, status, connection_id, created_at, closed_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_data['trigger_id'], user_data['user_id'], 'running', user_data['connection_id'], created_at, None))
    conn.commit()
    conn.close()

# gRPC Service Implementation
class IoTService(iot_service_pb2_grpc.IoTServiceServicer):
    def StartConnection(self, request, context):
        mqtt_userdata = {
            "user_id": request.user_id,
            "trigger_id": request.trigger_id,
            "connection_id": request.connection_id,
            "connection_url": request.connection_url,
            "port": request.port,
            "qos": request.qos,
            "keep_alive": request.keep_alive,
            "subscribe_topic": request.subscribe_topic,
        }

        threading.Thread(target=mqtt_connection_thread, args=(mqtt_userdata,)).start()
        return iot_service_pb2.ConnectionResponse(status="Connection started")

    def StopConnection(self, request, context):
        connection_key = f"{request.user_id}_{request.trigger_id}"
        if connection_key in user_connections:
            mqtt_client = user_connections.pop(connection_key)
            mqtt_client.loop_stop()
            mqtt_client.disconnect()

            closed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE connections
                    SET status = ?, closed_at = ?
                    WHERE trigger_id = ? AND user_id = ? AND connection_id = ?
                ''', ('ended', closed_at, request.trigger_id, request.user_id, request.connection_id))
                conn.commit()

            excel_filename = f"{request.user_id}_{request.trigger_id}_{request.connection_id}.xlsx"
            if os.path.exists(excel_filename):
                with open(excel_filename, "rb") as f:
                    file_data = f.read()
                return iot_service_pb2.StopConnectionResponse(status="Connection stopped", file_available=True, file_data=file_data)

        return iot_service_pb2.StopConnectionResponse(status="Connection not found", file_available=False)

    def GetConnectionStatus(self, request, context):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT status, created_at, closed_at
                FROM connections
                WHERE user_id = ? AND trigger_id = ?
            ''', (request.user_id, request.trigger_id))

            records = cursor.fetchall()

        response = [iot_service_pb2.ConnectionRecord(status=r[0], created_at=r[1], closed_at=r[2]) for r in records]
        return iot_service_pb2.ConnectionStatusResponse(connections=response)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    iot_service_pb2_grpc.add_IoTServiceServicer_to_server(IoTService(), server)
    server.add_insecure_port('[::]:50051')
    logging.info("Starting gRPC server on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    init_db()
    serve()
