import os
import json
import ast
import sys

import pandas as pd
import numpy as np

from constants import ATTRIBUTES, IDS

# get files object
with open("output_file_locations.json", "r") as f:
    files = json.load(f)

AYS_PIDS = files["AYS"]["participants"]
SUM_PIDS = files["SUM"]["participants"]
RT_PIDS = files["RT"]["participants"]
RTSUM_PIDS = files["RTSUM"]["participants"]

rows = []

print("CTRL ...")
for pid in AYS_PIDS:
    basepath = os.path.join("CTRL", pid)  # basepath for PID
    df = pd.read_csv(os.path.join(basepath, f"interaction.csv"))
    df = df[df['appMode'].isin(['politics', 'movies'])].reset_index(drop=True)
    rows.append([pid, 'CTRL', len(df.index)])

print("SUM ...")
for pid in SUM_PIDS:
    basepath = os.path.join("SUM", pid)  # basepath for PID
    df = pd.read_csv(os.path.join(basepath, f"interaction.csv"))
    df = df[df['appMode'].isin(['politics', 'movies'])].reset_index(drop=True)
    rows.append([pid, 'SUM', len(df.index)])

print("RT ...")
for pid in RT_PIDS:
    basepath = os.path.join("RT", pid)  # basepath for PID
    df = pd.read_csv(os.path.join(basepath, f"interaction.csv"))
    df = df[df['appMode'].isin(['politics', 'movies'])].reset_index(drop=True)
    rows.append([pid, 'RT', len(df.index)])

print("RTSUM ...")
for pid in RTSUM_PIDS:
    basepath = os.path.join("RTSUM", pid)  # basepath for PID
    df = pd.read_csv(os.path.join(basepath, f"interaction.csv"))
    df = df[df['appMode'].isin(['politics', 'movies'])].reset_index(drop=True)
    rows.append([pid, 'RTSUM', len(df.index)])

df = pd.DataFrame(
    rows,
    columns=['PID', 'Condition', '# Interaction Performed']
)
print(df.groupby('Condition').describe())
