import asyncio
import json
import uvicorn
from sse_starlette import EventSourceResponse
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

import redis

import time
import math

nb_vars = 8

NOMBRE_DE_POINTS = 1000

r = redis.Redis()

middleware = Middleware(CORSMiddleware, allow_origins=["*"], allow_headers=["*"])
server = Starlette(middleware=[middleware])

async def random_data():
    while True:
        await asyncio.sleep(0.1)

        timestamp = int(time.time()*1000)
        send_msg = {
                'timestamp': timestamp,
        }
        for j in range(nb_vars -1):
            send_msg["var_" + str(j)] = (math.sin((timestamp + j) / 1000) + j)
        # ajout de l'énuméré
        ts = (timestamp % 60000) / 1000
        if ts < 5:
            send_msg["var_7"] = "STOPPED"
        elif ts < 10:
            send_msg["var_7"] = "STARTING"
        else:
            send_msg["var_7"] = "RUNNING"

        dump = json.dumps(send_msg)
        # sauvegarder les x dernières valeurs dans redis
        r.rpush('random_data', dump)

        # shift la mémoire si points max atteints
        if r.llen('random_data') >= NOMBRE_DE_POINTS:
            r.lpop('random_data')

        yield dump

async def random_data_2():
    i = 0
    while True:
        await asyncio.sleep(0.1)

        timestamp = int(time.time()*1000)
        send_msg = {
                'timestamp': timestamp,
        }
        for j in range(nb_vars):
            send_msg["var_" + str(j)] = i % (j*100 + 1)

        if i < 10000:
            i+=1
        else:
            i =0
        dump = json.dumps(send_msg)
        # sauvegarder les x dernières valeurs dans redis
        r.rpush('random_data_2', dump)

        # shift la mémoire si points max atteints
        if r.llen('random_data_2') >= NOMBRE_DE_POINTS:
            r.lpop('random_data_2')

        yield dump

@server.route("/random_data")
async def sse(request):
    generator = random_data()
    return EventSourceResponse(generator)

@server.route("/random_data_2")
async def sse_2(request):
    generator = random_data_2()
    return EventSourceResponse(generator)

if __name__ == "__main__":
    uvicorn.run(server, port=5000)