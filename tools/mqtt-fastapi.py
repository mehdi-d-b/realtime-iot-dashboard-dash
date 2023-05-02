# -*- coding: utf-8 -*-
"""
Lancer avec uvicorn mqtt-fastapi:app --reload

Marche sur broker publique mais pas sur hbmqtt

@author: MB273828
"""

from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi import FastAPI
from fastapi_mqtt.config import MQTTConfig

app = FastAPI()

mqtt_config = MQTTConfig(host = "localhost",
    port= 1883,
    #keepalive = 60,
    #username="username",
    #password="strong_password"
    )

mqtt = FastMQTT(config=mqtt_config)

mqtt.init_app(app)

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("sinusoides_1") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    return 0

@mqtt.subscribe("sinusoides_1")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


@app.get("/")
async def func():
    mqtt.publish("/mqtt", "Hello from Fastapi") #publishing mqtt topic

    return {"result": True,"message":"Published" }