import paho.mqtt.client as mqtt
import mysql.connector
import json

from dotenv import load_dotenv
import os

load_dotenv()

# MQTT config
BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
TOPIC = os.getenv("MQTT_TOPIC")

# MySQL config
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    device_id = data["device_id"]
    temperature = data["temperature"]
    humidity = data["humidity"]

    print("Received:", data)

    # Insert into DB
    query = """
    INSERT INTO sensor_data (device_id, temperature, humidity)
    VALUES (%s, %s, %s)
    """
    values = (device_id, temperature, humidity)

    cursor.execute(query, values)
    db.commit()

client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)

client.loop_forever()