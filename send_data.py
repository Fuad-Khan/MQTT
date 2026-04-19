import paho.mqtt.client as mqtt
import json
import time

import paho.mqtt.client as mqtt
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
TOPIC = os.getenv("MQTT_TOPIC")

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

while True:
    payload = {
        "device_id": "sensor_1",
        "temperature": 25 + (time.time() % 5),
        "humidity": 60
    }

    client.publish(TOPIC, json.dumps(payload))
    print("Sent:", payload)

    time.sleep(2)