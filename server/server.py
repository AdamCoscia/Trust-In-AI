"""Server for interfacing with the frontend.
"""
import os
import time
from pathlib import Path

import pandas as pd
import socketio
from aiohttp import web
from aiohttp_index import IndexMiddleware

# from google.cloud import logging

# Set the path for the Google Cloud Logging logger
currdir = Path(__file__).parent.absolute()

# # USE FOR LUMOS
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(currdir, "lumos-logger-3a3d1c6114a4.json")

# # USE FOR LRG
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(currdir, "lrg-logger-dac0e4f3caf3.json")

# # Instantiates a client
# logging_client = logging.Client()

# # The name of the log to write to
# log_name = "lumos-logs"

# # Selects the log to write to
# logger = logging_client.logger(log_name)

# Deletes all logs for the logger
# logger.delete()

CLIENTS = {}  # entire data map of all client data
CLIENT_PARTICIPANT_ID_SOCKET_ID_MAPPING = {}
CLIENT_SOCKET_ID_PARTICIPANT_MAPPING = {}

SIO = socketio.AsyncServer()
APP = web.Application(middlewares=[IndexMiddleware()])
SIO.attach(APP)


def get_current_time():
    """Get current millis."""
    return int(round(time() * 1000))


@SIO.event
async def connect(sid, environ):
    print(f"Connected: {sid}")


@SIO.event
def disconnect(sid):
    if sid in CLIENT_SOCKET_ID_PARTICIPANT_MAPPING:
        pid = CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid]
        if pid in CLIENTS:
            CLIENTS[pid]["disconnected_at"] = get_current_time()
            print(f"Disconnected: Participant ID: {pid} | Socket ID: {sid}")


@SIO.event
async def on_session_end_page_level_logs(sid, payload):
    pid = payload["participantId"]
    if pid in CLIENTS and "data" in payload:
        dirname = f"output/{CLIENTS[pid]['app_type']}/{pid}"
        Path(dirname).mkdir(exist_ok=True)
        filename = f"output/{CLIENTS[pid]['app_type']}/{pid}/session_end_page_logs_{pid}_{get_current_time()}.tsv"
        df_to_save = pd.DataFrame(payload["data"])

        # persist to disk
        df_to_save.transpose().to_csv(filename, sep="\t")

        # # persist to google cloud logging
        # dict_obj = df_to_save.transpose().to_dict(orient="records")
        # log_obj = dict()
        # log_obj[pid + "_summary"] = json.dumps(dict_obj)
        # logger.log_struct(log_obj)

        print(f"Saved session logs to file: {filename}")


@SIO.event
async def on_save_logs(sid, data):
    if sid in CLIENT_SOCKET_ID_PARTICIPANT_MAPPING:
        pid = CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid]
        if pid in CLIENTS:
            dirname = f"output/{CLIENTS[pid]['app_type']}/{pid}"
            Path(dirname).mkdir(exist_ok=True)
            filename = f"output/{CLIENTS[pid]['app_type']}/{pid}/logs_{pid}_{get_current_time()}.tsv"
            df_to_save = pd.DataFrame(CLIENTS[pid]["response_list"])

            # persist to disk
            df_to_save.to_csv(filename, sep="\t")

            print(f"Saved logs to file: {filename}")


@SIO.event
async def on_interaction(sid, data):
    app_type = data["appType"]  # Condition {c1, c2, c3, c4}
    app_mode = data["appMode"]  # Task {service, practice}
    pid = data["participantId"]
    interaction_type = data["interactionType"]  # Interaction type - eg. hover, click

    # Let these get updated everytime an interaction occurs, to handle the
    #   worst case scenario of random restart of the server.
    CLIENT_SOCKET_ID_PARTICIPANT_MAPPING[sid] = pid
    CLIENT_PARTICIPANT_ID_SOCKET_ID_MAPPING[pid] = sid

    if pid not in CLIENTS:
        # new participant => establish data mapping for them!
        CLIENTS[pid] = {}
        CLIENTS[pid]["id"] = sid
        CLIENTS[pid]["participant_id"] = pid
        CLIENTS[pid]["app_mode"] = app_mode
        CLIENTS[pid]["app_type"] = app_type
        CLIENTS[pid]["connected_at"] = get_current_time()
        CLIENTS[pid]["response_list"] = []

    if app_mode != CLIENTS[pid]["app_mode"]:
        # datasets have been switched => reset the logs array!
        # OR
        # app_level (e.g. practice > live) is changed but same dataset is in use => reset the logs array!
        CLIENTS[pid]["app_mode"] = app_mode
        CLIENTS[pid]["response_list"] = []

    # record response to interaction
    response = {}
    response["sid"] = sid
    response["participant_id"] = pid
    response["app_mode"] = app_mode
    response["app_type"] = app_type
    response["processed_at"] = get_current_time()
    response["interaction_type"] = interaction_type
    response["input_data"] = data
    response["output_data"] = None

    # save response
    CLIENTS[pid]["response_list"].append(response)

    # # persist each interaction to google cloud logging
    # log_obj = dict()
    # log_obj[pid + "_interaction"] = json.dumps(response)
    # logger.log_struct(log_obj)

    await SIO.emit("log", response)  # send this to all
    await SIO.emit("interaction_response", response, room=sid)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    web.run_app(APP, port=port)
