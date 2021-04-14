import os
import json

import pandas as pd

# get files object
with open("output_file_locations.json", "r") as f:
    files = json.load(f)

CTRL_PIDS = files["CTRL"]["participants"]
WTHN_PIDS = files["WTHN"]["participants"]
BTWN_PIDS = files["BTWN"]["participants"]
BOTH_PIDS = files["BOTH"]["participants"]

rows = []

print("CTRL ...")
for pid in CTRL_PIDS:
    basepath = os.path.join("CTRL", pid)  # basepath for PID
    df = pd.read_csv(os.path.join(basepath, f"interactions.csv"))
    df = df[df['appMode'].isin(['hiring', 'movies'])].reset_index(drop=True)
    rows.append([pid, 'CTRL', len(df.index)])

print("WTHN ...")
for pid in WTHN_PIDS:
    basepath = os.path.join("WTHN", pid)  # basepath for PID
    df = pd.read_csv(os.path.join(basepath, f"interactions.csv"))
    df = df[df['appMode'].isin(['hiring', 'movies'])].reset_index(drop=True)
    rows.append([pid, 'WTHN', len(df.index)])

print("BTWN ...")
for pid in BTWN_PIDS:
    basepath = os.path.join("BTWN", pid)  # basepath for PID
    df = pd.read_csv(os.path.join(basepath, f"interactions.csv"))
    df = df[df['appMode'].isin(['hiring', 'movies'])].reset_index(drop=True)
    rows.append([pid, 'BTWN', len(df.index)])

print("BOTH ...")
for pid in BOTH_PIDS:
    basepath = os.path.join("BOTH", pid)  # basepath for PID
    df = pd.read_csv(os.path.join(basepath, f"interactions.csv"))
    df = df[df['appMode'].isin(['hiring', 'movies'])].reset_index(drop=True)
    rows.append([pid, 'BOTH', len(df.index)])

df = pd.DataFrame(
    rows,
    columns=['PID', 'Condition', '# interactions Performed']
)
print(df.groupby('Condition').describe())
