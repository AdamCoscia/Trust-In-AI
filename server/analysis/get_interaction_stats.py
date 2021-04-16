"""Calculates basic interaction statistics.
"""
import ast
import json
import os
import sys

import pandas as pd
import numpy as np

#
# ---------------------------- INTERACTION TYPES -----------------------------
# INITIALIZE_APP = "init_app"
# CARD_CLICKED = "card_clicked"
# GET_RECOMMENDATION = "get_recommendation"
# SAVE_SELECTION = "save_selection"
# CONTINUE = "continue"
# CLOSE_APP = "close_app"
#


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


def get_stats(df, task, pid):
    """"""

    # Count times particpant looked at recommendation before saving
    mask = df["interactionType"] == "get_recommendation"
    get_recs = df[mask]
    if len(get_recs.index) > 0:
        print(get_recs)
        
    sys.exit(0)

    # Combine attribute encode, filter, card toggle and pin dataframes
    dfs = []
    dfs = [df.set_index("attribute", drop=True).sort_index() for df in dfs]
    df_attr = pd.concat(dfs, axis=1, join="outer", copy=False).reset_index(drop=False)

    return df_attr


# get files object
with open("output_file_locations.json", "r") as f:
    files = json.load(f)

# 4 conditions to unpack
CTRL_PIDS = files["CTRL"]["participants"]
WTHN_PIDS = files["WTHN"]["participants"]
BTWN_PIDS = files["BTWN"]["participants"]
BOTH_PIDS = files["BOTH"]["participants"]

TASKS = ["hiring", "movies"]


# ================================= CTRL ================================= #

print("CTRL")
for task in TASKS:
    # lists of dataframes to combine into master file at the end per task
    ctrl_dfs = []

    # Loop through particpants
    for pid in CTRL_PIDS:
        basepath = os.path.join("CTRL", pid)  # basepath for PID
        print(f"  calculating {task} stats for CTRL PID {pid} ...")
        df = pd.read_csv(os.path.join(basepath, f"interactions.csv"))
        df_task = df[df["appMode"] == task].reset_index(drop=True).drop(columns=["appMode"])
        # get statistics
        df_stats = get_stats(df_task, task, pid)
        df_stats.to_csv(os.path.join(basepath, f"stats_{task}.csv"), index=False)
        df_stats.insert(0, "pid", pd.Series([pid for _ in range(6)]))
        ctrl_dfs.append(df_stats)

    # combine collected dataframes into master file at the end
    df_ctrl = pd.concat(ctrl_dfs)
    df_ctrl.to_csv(os.path.join("CTRL", f"all_CTRL_{task}_stats.csv"), index=False)
