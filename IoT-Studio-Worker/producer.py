import time
import random
import json
import paho.mqtt.client as mqtt

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.connect("broker.emqx.io", 1883)
mqttc.loop_start()

try:
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
        print(f"Sent message: {json_msg}")
        msg_info.wait_for_publish()

        time.sleep(1)

except KeyboardInterrupt:
    print("Publishing stopped by user.")

finally:
    mqttc.disconnect()
    mqttc.loop_stop()
