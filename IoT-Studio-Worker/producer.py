import time
import random
import json
import paho.mqtt.client as mqtt

# Define MQTT client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

try:
    # Connect to MQTT broker
    mqttc.connect("broker.emqx.io", 1883, 60)
    mqttc.loop_start()  # Start background loop

    while True:
        # Generate a dictionary with random values
        message = {
            "temperature": round(random.uniform(20.0, 30.0), 2),  # Random float between 20 and 30
            "humidity": random.randint(30, 80),  # Random integer between 30 and 80
            "light": random.choice(["ON", "OFF"]),  # Randomly choose between ON and OFF
            "status": random.choice(["normal", "warning", "critical"]),  # Random status
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
        }

        # Convert dictionary to JSON string
        json_msg = json.dumps(message)

        # Publish the JSON message
        msg_info = mqttc.publish("paho/test/topic", json_msg, qos=1)
        msg_info.wait_for_publish()  # Ensure the message is published
        print(f"Sent message: {json_msg}")

        time.sleep(1)  # Sleep for 1 second

except KeyboardInterrupt:
    print("\nPublishing stopped by user.")

except Exception as e:
    print(f"Error: {str(e)}")

finally:
    print("Disconnecting from broker...")
    mqttc.disconnect()
    mqttc.loop_stop()
