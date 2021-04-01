"""Server for interfacing with the frontend.
"""
import json
import os
import time
import urllib.parse as urlparse

import pandas as pd
import redis
import socketio
from aiohttp import web
from aiohttp_index import IndexMiddleware

DEPLOY_MODE = "local"  # local / heroku
print(f'deploy mode => {DEPLOY_MODE}')

if DEPLOY_MODE == "local":
    # for when developing locally
    keys = json.load(open("redis.json", "r"))  #  stored remotely for safety
    if keys:
        print("Connecting to redis server", end='\r')
        r = redis.Redis(host=keys["hostname"], password=keys["password"], port=keys["port"])
        while not r.ping():
            time.sleep(1.0)
    else:
        raise FileNotFoundError('Count not load redis.json')

elif DEPLOY_MODE == "heroku":
    # for when pushing to heroku
    if os.environ.get("REDISCLOUD_URL"):
        print("Connecting to redis server ...", end='\r')
        url = urlparse.urlparse(os.environ.get("REDISCLOUD_URL"))
        r = redis.Redis(host=url.hostname, port=url.port, password=url.password)
        while not r.ping():
            time.sleep(1.0)
    else:
        raise FileNotFoundError('REDISCLOUD_URL not found.')

print("Connected ")

CLIENTS = {}  # entire data map of all client data
CLIENT_PARTICIPANT_ID_SOCKET_ID_MAPPING = {}
CLIENT_SOCKET_ID_PARTICIPANT_MAPPING = {}

SIO = socketio.AsyncServer()
APP = web.Application(middlewares=[IndexMiddleware()])
SIO.attach(APP)


def get_current_time():
    """Get current millis since EPOCH."""
    return int(time.time())


@SIO.event
async def connect(sid):
    print(f"Connected: Socket ID: {sid}")


@SIO.event
def disconnect(sid):
    try:
        pid = CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid]
        CLIENTS[pid]["disconnected_at"] = get_current_time()
        print(f"Disconnected: Participant ID: {pid} | Socket ID: {sid}")
    except Exception as e:
        print(e)


@SIO.event
async def save_session_logs(sid, data):
    try:
        pid = data["participantId"]  # get participant ID
        logs = data["logs"]  # session page times
        if DEPLOY_MODE == "heroku":
            payload = json.dumps(logs)
            r.rpush(f"user:{pid}:interactions", payload)
            r.sadd("users", pid)
        elif DEPLOY_MODE == "local":
            dirpath = os.path.join("output", pid)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            filepath = os.path.join(dirpath, f"session_timestamps.csv")
            pd.DataFrame(logs).to_csv(filepath, index=False)
            print(f"Saved session logs to file: {filepath}")
    except Exception as e:
        print(e)


@SIO.event
async def save_interaction_logs(sid):
    if DEPLOY_MODE == "local":
        try:
            pid = CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid]
            interactions = CLIENTS[pid]["response_list"]
            dirpath = os.path.join("output", pid)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            filepath = os.path.join(dirpath, f"interactions.csv")
            pd.DataFrame(interactions).to_csv(filepath, index=False)
            print(f"Saved interaction logs to file: {filepath}")
        except Exception as e:
            print(e)


@SIO.event
async def on_interaction(sid, data):
    pid = data["participantId"]

    # record response to interaction
    response = {}
    response["sid"] = sid  # server ID
    response["processed_at"] = get_current_time()  # since EPOCH
    response["inputs"] = data  # from client

    # Let these get updated everytime an interaction occurs, to handle the
    #   worst case scenario of random restart of the server.
    CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid] = pid
    CLIENT_PARTICIPANT_ID_SOCKET_ID_MAPPING[pid] = sid

    if pid not in CLIENTS:
        # new participant => establish data mapping for them!
        CLIENTS[pid] = {}
        CLIENTS[pid]["sid"] = sid
        CLIENTS[pid]["connected_at"] = get_current_time()
        CLIENTS[pid]["response_list"] = []

    # save response
    CLIENTS[pid]["response_list"].append(response)

    # persist each interaction to redis
    payload = json.dumps(response)
    r.rpush(f"user:{pid}:interactions", payload)
    r.sadd("users", pid)

    await SIO.emit("log", response)  # send this to all
    await SIO.emit("interaction_response", response, room=sid)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    web.run_app(APP, port=port)
