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
print(f"deploy mode => {DEPLOY_MODE}")

if DEPLOY_MODE == "local":
    # for when developing locally
    keys = json.load(open("redis.json", "r"))  #  stored remotely for safety
    if keys:
        print("Connecting to redis server", end="\r")
        r = redis.Redis(host=keys["hostname"], password=keys["password"], port=keys["port"])
        while not r.ping():
            time.sleep(1.0)
    else:
        raise FileNotFoundError("Count not load redis.json")

elif DEPLOY_MODE == "heroku":
    # for when pushing to heroku
    if os.environ.get("REDISCLOUD_URL"):
        print("Connecting to redis server ...", end="\r")
        url = urlparse.urlparse(os.environ.get("REDISCLOUD_URL"))
        r = redis.Redis(host=url.hostname, port=url.port, password=url.password)
        while not r.ping():
            time.sleep(1.0)
    else:
        raise FileNotFoundError("REDISCLOUD_URL not found.")

print("Connected ")


CLIENT_PARTICIPANT_ID_SOCKET_ID_MAPPING = {}
CLIENT_SOCKET_ID_PARTICIPANT_MAPPING = {}

SIO = socketio.AsyncServer(cors_allowed_origins="*")
APP = web.Application(middlewares=[IndexMiddleware()])
SIO.attach(APP)


def get_current_time():
    """Get current millis since EPOCH."""
    return int(time.time())


@SIO.event
def connect(sid, environ, auth):
    print(f"Connected: Socket ID: {sid}")


@SIO.event
def disconnect(sid):
    if sid in CLIENT_SOCKET_ID_PARTICIPANT_MAPPING:
        pid = CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid]
    else:
        pid = "unknown"
    print(f"Disconnected: Participant ID: {pid} | Socket ID: {sid}")


@SIO.event
async def save_session_log(sid, data):
    try:
        pid = data["pid"]  # get participant ID
        CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid] = pid  # update pid reference
        CLIENT_PARTICIPANT_ID_SOCKET_ID_MAPPING[pid] = sid  # update sid reference
        log = data["log"]  # session page times
        payload = json.dumps(log)  # object to JSON
        r.set(f"user:{pid}:session", payload)
        r.sadd("users", pid)
    except Exception as e:
        print(e)


@SIO.event
async def save_selection_log(sid, data):
    try:
        pid = data["pid"]  # get participant ID
        CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid] = pid  # update pid reference
        CLIENT_PARTICIPANT_ID_SOCKET_ID_MAPPING[pid] = sid  # update sid reference
        log = data["log"]  # selections for appMode
        payload = json.dumps(log)  # object to JSON
        r.rpush(f"user:{pid}:selections", payload)
        r.sadd("users", pid)
    except Exception as e:
        print(e)


@SIO.event
async def on_interaction(sid, data):
    # Get client PID
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

    # persist each interaction to redis
    payload = json.dumps(response)
    r.rpush(f"user:{pid}:interactions", payload)
    r.sadd("users", pid)

    await SIO.emit("interaction_response", response, room=sid)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    web.run_app(APP, port=port)
