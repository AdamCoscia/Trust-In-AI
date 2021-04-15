import ast
import json
import os
import sys

import pandas as pd
import numpy as np


def get_dict(x):
    try:
        return ast.literal_eval(str(x))
    except Exception as e:
        return np.NaN


def get_list(x):
    try:
        return ast.literal_eval(str(x))
    except Exception as e:
        return []


def unpack_session_log(file):
    """Unpacks session_log.json for each participant and produces EPOCH timestamps
    for each completed activity.

    Returns dataframe of timestamps and app order as string use in filename.
    """
    df = pd.read_csv(file)
    # get app order
    app_order_list = df.at[0, "appOrder"]
    if app_order_list.index("hiring") > app_order_list.index("movies"):
        app_order = "MH"
    elif app_order_list.index("movies") > app_order_list.index("hiring"):
        app_order = "HM"
    else:
        app_order = "unknown"
    # filter out all columns that aren't activities
    df_activities = (
        df.drop(columns=["participantId", "appOrder", "appType", "appMode"])
        .T.reset_index()
        .rename(columns={"index": "activity"})
    )
    # get epoch conversion of timestamps => timestamps already in in GMT-05:00 or "US/Eastern" (Georgia Tech Time)
    df_activities_ts = pd.concat(
        [df_activities["activity"], df_activities[0].map(lambda x: get_dict(x)).apply(pd.Series)["timestamp"]],
        axis=1,
    )
    return df_activities_ts, app_order


def unpack_selections(file):
    """Unpacks selections, pivots file.

    Returns dataframe.
    """
    df = pd.read_csv(file)

    # Explode the selections into a full table and assign task number
    df_selections = (
        df.set_index("appMode")["selections"]
        .map(lambda x: get_list(x))
        .explode()
        .map(lambda x: get_dict(x))
        .apply(pd.Series)
        .reset_index()
        .groupby("appMode", as_index=False)
        .apply(lambda x: x.reset_index(drop=True))
        .sort_values("savedAt")
        .reset_index()
        .drop(columns=["level_0"])
        .rename(columns={"level_1": "task"})
    )

    return df_selections


def unpack_interactions(file):
    """Unpacks interaction data.

    Returns dataframe.
    """

    #
    # All Columns (3) to work with:
    #   'sid': String
    #   'processed_at': Integer
    #   'input': String(JSON) => unpacked below as `input` (26 columns)
    #
    df = pd.read_csv(file)

    #
    # (7) Input columns possible to work with:
    #
    #   'participantId': String
    #   'appMode': String
    #   'interactionAt': Integer
    #   'interactionType': String
    #   'currentScenario': Integer
    #   'selectedId': Integer
    #   'recommendationShown': Boolean
    #
    data = df["inputs"].map(lambda x: get_dict(x)).apply(pd.Series)

    return data


if __name__ == "__main__":
    # get files object
    with open("output_file_locations.json", "r") as f:
        files = json.load(f)

    # 4 conditions to unpack
    CTRL = files["CTRL"]
    WTHN = files["WTHN"]
    BTWN = files["BTWN"]
    BOTH = files["BOTH"]

    print("CTRL")
    for i in range(len(CTRL["participants"])):
        pid = CTRL["participants"][i]  # get PID
        print(f"({i+1}/{len(CTRL['participants'])}) {pid}")
        if not os.path.exists(os.path.join("CTRL", pid)):
            os.mkdir(os.path.join("CTRL", pid))
        # unpack session_log (timestamps)
        data_timestamps, app_order = unpack_session_log(CTRL[pid]["session_log"])
        filepath = os.path.join("CTRL", pid, f"timestamps.csv")
        data_timestamps.to_csv(filepath, index=False)
        # unpack selections
        data_selections = unpack_selections(CTRL[pid]["selections"])
        filepath = os.path.join("CTRL", pid, f"selections.csv")
        data_selections.to_csv(filepath, index=False)
        # unpack interactions
        data_interactions = unpack_interactions(CTRL[pid]["interactions"])
        filepath = os.path.join("CTRL", pid, "interactions.csv")
        data_interactions.to_csv(filepath, index=False)

    print("WTHN")
    for i in range(len(WTHN["participants"])):
        pid = WTHN["participants"][i]  # get PID
        print(f"({i+1}/{len(WTHN['participants'])}) {pid}")
        if not os.path.exists(os.path.join("WTHN", pid)):
            os.mkdir(os.path.join("WTHN", pid))
        # unpack session_log (timestamps)
        data_timestamps, app_order = unpack_session_log(WTHN[pid]["session_log"])
        filepath = os.path.join("WTHN", pid, f"timestamps.csv")
        data_timestamps.to_csv(filepath, index=False)
        # unpack selections
        data_selections = unpack_selections(WTHN[pid]["selections"])
        filepath = os.path.join("WTHN", pid, f"selections.csv")
        data_selections.to_csv(filepath, index=False)
        # unpack interactions
        data_interactions = unpack_interactions(WTHN[pid]["interactions"])
        filepath = os.path.join("WTHN", pid, "interactions.csv")
        data_interactions.to_csv(filepath, index=False)

    print("BTWN")
    for i in range(len(BTWN["participants"])):
        pid = BTWN["participants"][i]  # get PID
        print(f"({i+1}/{len(BTWN['participants'])}) {pid}")
        if not os.path.exists(os.path.join("BTWN", pid)):
            os.mkdir(os.path.join("BTWN", pid))
        # unpack session_log (timestamps)
        data_timestamps, app_order = unpack_session_log(BTWN[pid]["session_log"])
        filepath = os.path.join("BTWN", pid, f"timestamps.csv")
        data_timestamps.to_csv(filepath, index=False)
        # unpack selections
        data_selections = unpack_selections(BTWN[pid]["selections"])
        filepath = os.path.join("BTWN", pid, f"selections.csv")
        data_selections.to_csv(filepath, index=False)
        # unpack interactions
        data_interactions = unpack_interactions(BTWN[pid]["interactions"])
        filepath = os.path.join("BTWN", pid, "interactions.csv")
        data_interactions.to_csv(filepath, index=False)

    print("BOTH")
    for i in range(len(BOTH["participants"])):
        pid = BOTH["participants"][i]  # get PID
        print(f"({i+1}/{len(BOTH['participants'])}) {pid}")
        if not os.path.exists(os.path.join("BOTH", pid)):
            os.mkdir(os.path.join("BOTH", pid))
        # unpack session_log (timestamps)
        data_timestamps, app_order = unpack_session_log(BOTH[pid]["session_log"])
        filepath = os.path.join("BOTH", pid, f"timestamps.csv")
        data_timestamps.to_csv(filepath, index=False)
        # unpack selections
        data_selections = unpack_selections(BOTH[pid]["selections"])
        filepath = os.path.join("BOTH", pid, f"selections.csv")
        data_selections.to_csv(filepath, index=False)
        # unpack interactions
        data_interactions = unpack_interactions(BOTH[pid]["interactions"])
        filepath = os.path.join("BOTH", pid, "interactions.csv")
        data_interactions.to_csv(filepath, index=False)
