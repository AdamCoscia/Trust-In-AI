"""Server for interfacing with the frontend.
"""
import json
import os
import time
import urllib.parse as urlparse
from itertools import cycle

import redis
import socketio
from aiohttp import web
from aiohttp_index import IndexMiddleware

# APP_STATES = cycle(
#     [
#         {"appOrder": ["practice", "movies", "hiring"], "appType": "BTWN"},
#         {"appOrder": ["practice", "hiring", "movies"], "appType": "BOTH"},
#         {"appOrder": ["practice", "movies", "hiring"], "appType": "CTRL"},
#         {"appOrder": ["practice", "movies", "hiring"], "appType": "WTHN"},
#         {"appOrder": ["practice", "hiring", "movies"], "appType": "BTWN"},
#         {"appOrder": ["practice", "hiring", "movies"], "appType": "WTHN"},
#         {"appOrder": ["practice", "hiring", "movies"], "appType": "CTRL"},
#         {"appOrder": ["practice", "movies", "hiring"], "appType": "BOTH"},
#     ]
# )

APP_STATES = cycle(
    [
        {"appOrder": ["practice", "hiring", "movies"], "appType": "BOTH"},
        {"appOrder": ["practice", "movies", "hiring"], "appType": "CTRL"},
        {"appOrder": ["practice", "hiring", "movies"], "appType": "CTRL"},
        {"appOrder": ["practice", "movies", "hiring"], "appType": "BOTH"},
    ]
)

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
    if sid in CLIENT_SOCKET_ID_PARTICIPANT_MAPPING:
        pid = CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid]
    else:
        pid = "unknown     "
    print(f"      Connected | SID: {sid} | PID: {pid}")


@SIO.event
def disconnect(sid):
    if sid in CLIENT_SOCKET_ID_PARTICIPANT_MAPPING:
        pid = CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid]
    else:
        pid = "unknown     "
    print(f"   Disconnected | SID: {sid} | PID: {pid}")


@SIO.event
async def save_session_log(sid, data):
    try:
        pid = data["pid"]  # get PID
        CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid] = pid  # update pid reference
        CLIENT_PARTICIPANT_ID_SOCKET_ID_MAPPING[pid] = sid  # update sid reference
        log = data["log"]  # session page times
        payload = json.dumps(log)  # object to JSON
        R.set(f"user:{pid}:session", payload)
        R.sadd("users", pid)
        print(f"  Session Saved | SID: {sid} | PID: {pid}")
    except Exception as e:
        print(e)


@SIO.event
async def save_selection_log(sid, data):
    try:
        pid = data["pid"]  # get PID
        CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid] = pid  # update pid reference
        CLIENT_PARTICIPANT_ID_SOCKET_ID_MAPPING[pid] = sid  # update sid reference
        log = data["log"]  # selections for appMode
        payload = json.dumps(log)  # object to JSON
        R.rpush(f"user:{pid}:selections", payload)
        R.sadd("users", pid)
        print(f"Selection Saved | SID: {sid} | PID: {pid}")
    except Exception as e:
        print(e)


@SIO.event
async def get_new_app_state(sid, data):
    # Get client PID
    pid = data["participantId"]

    # Let these get updated everytime an interaction occurs, to handle the
    #   worst case scenario of random restart of the server.
    CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid] = pid
    CLIENT_PARTICIPANT_ID_SOCKET_ID_MAPPING[pid] = sid

    # get next app state in the cycle
    new_app_state = next(APP_STATES)
    print(
        f" New Type/Order | SID: {sid} | PID: {pid} | appType: {new_app_state['appType']} | appOrder: {new_app_state['appOrder']}"
    )

    await SIO.emit("new_app_state_response", new_app_state, room=sid)


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
    R.rpush(f"user:{pid}:interactions", payload)
    R.sadd("users", pid)

    await SIO.emit("interaction_response", response, room=sid)


if __name__ == "__main__":
    # Collect redis url endpoint
    try:
        url = json.load(open("redis.json", "r"))  #  stored remotely for safety
        hostname, port, password = url["hostname"], url["port"], url["password"]
    except FileNotFoundError as e:
        if "REDISCLOUD_URL" in os.environ and os.environ.get("REDISCLOUD_URL"):
            url = urlparse.urlparse(os.environ.get("REDISCLOUD_URL"))
            hostname, port, password = url.hostname, url.port, url.password
        else:
            raise KeyError("'REDISCLOUD_URL' not found in environment variables.")

    # Connect to redis client
    print("Connecting to redis server", end="\r")
    try:
        R = redis.Redis(host=hostname, port=port, password=password)
        R.ping()
        print(f"Connected  ")
    except redis.RedisError as e:
        raise e

    # Run the web server
    port = int(os.environ.get("PORT", 3000))
    web.run_app(APP, port=port)
