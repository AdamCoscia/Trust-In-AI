import os
import json
import ast

import pandas as pd
import numpy as np


def get_bias_interactions(df):
    """Collects only bias interactions from cleaned interaction logs.

    Returns dataframe of only those interactions.
    """
    bias_interactions = [
        "mouseout",
        "add_to_list_via_card_click",
        "add_to_list_via_scatterplot_click",
        "mouseout_from_list",
        "remove_from_list_via_card_click",
        "remove_from_list_via_list_item_click",
    ]
    mask = df["interactionType"].isin(bias_interactions)
    df_bias_interactions = df[mask].reset_index(drop=True)
    return df_bias_interactions


# get files object
with open("output_file_locations.json", "r") as f:
    files = json.load(f)

AYS_PIDS = files["AYS"]["participants"]
SUM_PIDS = files["SUM"]["participants"]
RT_PIDS = files["RT"]["participants"]
RTSUM_PIDS = files["RTSUM"]["participants"]

# AYS
print("AYS")
for pid in AYS_PIDS:
    basepath = os.path.join("CTRL", pid)  # basepath for PID
    print(f"  collecting bias interactions for AYS PID {pid} ...")
    df = pd.read_csv(os.path.join(basepath, f"interaction.csv"))
    df_bias_interactions = get_bias_interactions(df)
    # print(df_bias_interactions)
    df_bias_interactions.to_csv(os.path.join(basepath, f"bias_interaction.csv"), index=False)

# SUM
print("SUM")
for pid in SUM_PIDS:
    basepath = os.path.join("SUM", pid)  # basepath for PID
    print(f"  collecting bias interactions for SUM PID {pid} ...")
    df = pd.read_csv(os.path.join(basepath, f"interaction.csv"))
    df_bias_interactions = get_bias_interactions(df)
    # print(df_bias_interactions)
    df_bias_interactions.to_csv(os.path.join(basepath, f"bias_interaction.csv"), index=False)

# RT
print("RT")
for pid in RT_PIDS:
    basepath = os.path.join("RT", pid)  # basepath for PID
    print(f"  collecting bias interactions for RT PID {pid} ...")
    df = pd.read_csv(os.path.join(basepath, f"interaction.csv"))
    df_bias_interactions = get_bias_interactions(df)
    # print(df_bias_interactions)
    df_bias_interactions.to_csv(os.path.join(basepath, f"bias_interaction.csv"), index=False)

# RTSUM
print("RTSUM")
for pid in RTSUM_PIDS:
    basepath = os.path.join("RTSUM", pid)  # basepath for PID
    print(f"  collecting bias interactions for RTSUM PID {pid} ...")
    df = pd.read_csv(os.path.join(basepath, f"interaction.csv"))
    df_bias_interactions = get_bias_interactions(df)
    # print(df_bias_interactions)
    df_bias_interactions.to_csv(os.path.join(basepath, f"bias_interaction.csv"), index=False)
