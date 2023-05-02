# -*- coding: utf-8 -*-
"""
Lancer ce script manuellement pour publier des sinusoides aléatoires
dans un topic MQTT, dans le broker lancé par "start_local_broker.py".

@author: MB273828
"""

import paho.mqtt.client as mqtt
import threading
import time
import math
import orjson as json
import random
import logging

nb_topics = 1
nb_vars = 8

# Logging
logger = logging.getLogger(__name__)
formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
logging.basicConfig(level=logging.INFO, format=formatter)

# Variables MQTT
MQTT_SERVER = 'localhost'
MQTT_SERVER_PORT = 1883
MQTT_TOPICS = ['sinusoides_' + str(x + 1) for x in range(nb_topics)]

# Connexion
client = mqtt.Client()
client.connect(MQTT_SERVER, MQTT_SERVER_PORT)
logger.info('Connected!')    

# Boucle de publication
while True:
    timestamp = int(time.time()*1000)
    
    for i in range(nb_topics):
        send_msg = {
                'timestamp': timestamp,
        }
        for j in range(nb_vars):
            send_msg["var_" + str(j)] = (50 * math.sin(timestamp / random.randint(50,1000)) + 1)
        client.publish(MQTT_TOPICS[i], payload=json.dumps(send_msg))
    time.sleep(1)
            