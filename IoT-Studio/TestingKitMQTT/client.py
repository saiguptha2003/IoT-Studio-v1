import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}")
    client.subscribe("paho/test/topic")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost", 1883, 60)
mqttc.loop_forever()
