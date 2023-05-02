# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 14:28:37 2023

Lancer un broker local pour tests MQTT

@author: MB273828
"""

import multiprocessing as mp
import scripts.broker_script
import time
import os,sys
import asyncio
from hbmqtt.broker import Broker


# du code pour démarrer le broker mqtt full python
# directement à partir du main
def run_the_broker():
    if True:
       
        config = {
            'listeners': {
                'default': {
                    'type': 'tcp',
                    'bind': '127.0.0.1:1883',
                },
            },
            'sys_interval': 10,
            'auth': {
                'allow-anonymous': True,
                'plugins': [
                    'auth_file', 'auth_anonymous'
                ]
            },
            'topic-check': {
                'enabled': True,
                "plugins": ["topic_taboo"]
            }
        }

        loop = asyncio.get_event_loop()
        broker = Broker(config)
        try:
            loop.run_until_complete(broker.start())
            loop.run_forever()
        except KeyboardInterrupt:
            loop.run_until_complete(broker.shutdown())
        finally:
            loop.close()

        scripts.broker_script.main()
    else:
        pass


# à regarder : https://github.com/beerfactory/hbmqtt/issues/211
# pour mettre le broker dnas un thread

run_the_broker()    
