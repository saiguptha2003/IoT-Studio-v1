import io
import zipfile

def create_zip_file(topic, port, keep_alive):
    """Generate all files dynamically and create a ZIP package in memory."""
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        env_content = f"MQTT_TOPIC={topic}\nMQTT_PORT={port}\nMQTT_KEEP_ALIVE={keep_alive}\n"
        zipf.writestr(".env", env_content)
        mqtt_client_content = """import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import signal
import sys

# Load environment variables
load_dotenv()
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "test/topic")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_KEEP_ALIVE = int(os.getenv("MQTT_KEEP_ALIVE", 60))

# Create the MQTT client
mqttc = mqtt.Client()

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    # Unpack the message payload (decode it from byte format to string)
    message = msg.payload.decode()  # This decodes the byte string into a readable format
    print(f"{message}")  # Display the decoded message

def signal_handler(sig, frame):
    print("Exiting MQTT client...")
    mqttc.disconnect()  # Properly disconnect the client
    sys.exit(0)  # Exit the program

# Register the signal handler for graceful shutdown on Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Assign the callback functions
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Connect to the broker
mqttc.connect("localhost", MQTT_PORT, MQTT_KEEP_ALIVE)

try:
    # Start the MQTT loop to process network events
    mqttc.loop_forever()
except KeyboardInterrupt:
    # If Ctrl+C is pressed, the signal_handler will handle the shutdown
    pass
"""
        zipf.writestr("mqtt_client.py", mqtt_client_content)

        zipf.writestr("requirements.txt", "paho-mqtt\ndotenv\n")
        dockerfile_content = """FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "mqtt_client.py"]
"""
        zipf.writestr("Dockerfile", dockerfile_content)
        docker_compose_content = f"""version: '3.8'
services:
  mqtt-client:
    build: .
    environment:
        - .env
    restart: always
"""
        zipf.writestr("docker-compose.yml", docker_compose_content)
        readme_content = f"""# MQTT Client

## 📌 Setup

1. The `.env` file is already included with the MQTT settings:
   ```
   MQTT_TOPIC={topic}
   MQTT_PORT={port}
   MQTT_KEEP_ALIVE={keep_alive}
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run using Python:
   ```bash
   python mqtt_client.py
   ```

## 🐳 Docker Setup

1. Build and run using Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. Or build and run using Docker directly:
   ```bash
   docker build -t mqtt-client .
   docker run mqtt-client
   ```

## 📝 Configuration
- MQTT Topic: {topic}
- MQTT Port: {port}
- Keep Alive: {keep_alive} seconds
"""
        zipf.writestr("README.md", readme_content)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()