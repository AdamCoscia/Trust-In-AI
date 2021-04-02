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

users = [u.decode("utf-8") for u in r.smembers("users")]
user_logs = {
    u: {
        "interactions": [json.loads(l) for l in r.lrange(f"user:{u}:interactions", 0, -1)],
        "selections": [json.loads(l) for l in r.lrange(f"user:{u}:selections", 0, -1)],
        "session_log": [json.loads(r.get(f"user:{u}:session"))],
    }
    for u in users
}

print("=== SUMMARY ===\n")

if len(users) == 0:
    print("No users.")
else:
    for pid in users:
        print(pid)
        print("-" * len(pid))
        # Create output directory
        if not os.path.exists(os.path.join("output", pid)):
            os.makedirs(os.path.join("output", pid))
        # Save interactions
        df = pd.DataFrame.from_records(user_logs[pid]["interactions"])
        df.to_csv(os.path.join("output", pid, "interactions.csv"), index=False)
        print(df.head(), end="\n")
        # Save selections
        df = pd.DataFrame.from_records(user_logs[pid]["selections"])
        df.to_csv(os.path.join("output", pid, "selections.csv"), index=False)
        print(df.head(), end="\n")
        # Save session log
        df = pd.DataFrame(user_logs[pid]["session_log"])
        df.to_csv(os.path.join("output", pid, "session_log.csv"), index=False)
        print(df.head(), end="\n")
        # Delete keys off redis
        r.delete(f"user:{pid}:interactions")
        r.delete(f"user:{pid}:selections")
        r.delete(f"user:{pid}:session")

# delete users set of redis
r.delete("users")
