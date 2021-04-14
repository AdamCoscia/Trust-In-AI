import os
import json


CONDITIONS = ["CTRL", "WTHN", "BTWN", "BOTH"]  # conditions in the study
PIDS_TO_EXCLUDE = []  # these PIDs should NOT be used!
FILES = {}  # { condition: { pid: { logs_practice: [], logs_live: [], ... } ... } ...}

for condition in CONDITIONS:
    FILES[condition] = {
        "participants": [],
    }
    # walk through directories
    for path, directories, files in os.walk(os.path.join("..", "output", condition)):
        if not directories:
            # reached folder with no sub-folders and files => get participant files
            pid = os.path.basename(os.path.normpath(path))
            if not pid in PIDS_TO_EXCLUDE and not pid in CONDITIONS:
                FILES[condition]["participants"].append(pid)
                FILES[condition][pid] = {
                    "interactions": "",
                    "selections": "",
                    "session_log": "",
                    "file_unknown": [],
                }
                for file in files:
                    if file == "interactions.csv":
                        FILES[condition][pid]["interactions"] = os.path.join(path, file)
                    elif file == "selections.csv":
                        FILES[condition][pid]["selections"] = os.path.join(path, file)
                    elif file == "session_log.csv":
                        FILES[condition][pid]["session_log"] = os.path.join(path, file)
                    elif file == ".gitkeep":
                        pass  # ignore
                    else:
                        print(f"[WARN] Unknown file found for {pid}: {file}")
                        FILES[condition][pid]["file_unknown"].append(os.path.join(path, file))

with open("output_file_locations.json", "w") as fp:
    json.dump(FILES, fp)
