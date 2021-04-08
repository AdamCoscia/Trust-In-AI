import json
import os
import time
import sys

import redis
import pandas as pd

keys = json.load(open("redis.json", "r"))  #  stored remotely for safety

# === Establish Connection === #

sys.stdout.write(f"\rConnecting to {keys['hostname']}")
sys.stdout.flush()
r = redis.Redis(host=keys["hostname"], password=keys["password"], port=keys["port"])
while not r.ping():
    for c in ["|", "/", "-", "\\"]:
        sys.stdout.write(f"\rConnecting to {keys['hostname']} ... {c}")
        sys.stdout.flush()
        time.sleep(0.33)
sys.stdout.write(f"\rConnecting to {keys['hostname']} ... Connected!\n")
sys.stdout.flush()

#
# GET Operations for different data types:
#   if value is of type string -> GET <key>
#   if value is of type hash -> HGETALL <key>
#   if value is of type lists -> lrange <key> <start> <end>
#   if value is of type sets -> smembers <key>
#   if value is of type sorted sets -> ZRANGEBYSCORE <key> <min> <max>
#

sys.stdout.write(f"\rFetching user data ...")
sys.stdout.flush()

users = []
user_logs = {}
if r.smembers("users"):
    users = [u.decode("utf-8") for u in r.smembers("users")]
    for u in users:
        user_logs[u] = {"interactions": None, "selections": None, "session_log": None}
        if r.lrange(f"user:{u}:interactions", 0, -1):
            user_logs[u]["interactions"] = [json.loads(l) for l in r.lrange(f"user:{u}:interactions", 0, -1)]
        if r.lrange(f"user:{u}:selections", 0, -1):
            user_logs[u]["selections"] = [json.loads(l) for l in r.lrange(f"user:{u}:selections", 0, -1)]
        if r.get(f"user:{u}:session"):
            user_logs[u]["session_log"] = (json.loads(r.get(f"user:{u}:session")),)

sys.stdout.write(f"\rFetching user data ... Complete!\n")
sys.stdout.flush()

print("=== SUMMARY ===")

if len(users) == 0:
    print("No users.")
else:
    print(f"{len(users)} users' data pulled:\n")
    for pid in users:
        print(pid)
        print("-" * len(pid))

        # Use session log to get user appType for sorting outputs
        if user_logs[pid]["session_log"]:
            df = pd.DataFrame(user_logs[pid]["session_log"])
            app_type = df.at[0, "appType"]  # get appType
            # create output directory
            if not os.path.exists(os.path.join("output", app_type, pid)):
                os.makedirs(os.path.join("output", app_type, pid))
            df.to_csv(os.path.join("output", app_type, pid, "session_log.csv"), index=False)
            print("     Session log | Yes")
            r.delete(f"user:{pid}:session")
        else:
            app_type = "unknown"
            # create output directory
            if not os.path.exists(os.path.join("output", app_type, pid)):
                os.makedirs(os.path.join("output", app_type, pid))
            print("     Session log | No")

        # Save interactions
        if user_logs[pid]["interactions"]:
            df = pd.DataFrame.from_records(user_logs[pid]["interactions"])
            df.to_csv(os.path.join("output", app_type, pid, "interactions.csv"), index=False)
            print("Interactions Log | Yes")
            r.delete(f"user:{pid}:interactions")
        else:
            print("Interactions Log | No")

        # Save selections
        if user_logs[pid]["selections"]:
            df = pd.DataFrame.from_records(user_logs[pid]["selections"])
            df.to_csv(os.path.join("output", app_type, pid, "selections.csv"), index=False)
            print("  Selections Log | Yes")
            r.delete(f"user:{pid}:selections")
        else:
            print("  Selections Log | No")

    # delete users set of redis
    r.delete("users")
