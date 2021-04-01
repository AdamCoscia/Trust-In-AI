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
    for c in ['|', '/', '-', '\\']:
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
interactions = {u: [json.loads(l) for l in r.lrange(f"user:{u}:interactions", 0, -1)] for u in users}
session_end_pages = {u: [json.loads(l) for l in r.lrange(f"user:{u}:interactions", 0, -1)] for u in users}

print("=== SUMMARY ===\n")

if len(users) == 0:
    print("No users.")
else:
    for pid in users:
        print(pid)
        print("-" * len(pid))
        df = pd.DataFrame.from_records(interactions[pid])
        if not os.path.exists(os.path.join("output", pid)):
            os.makedirs(os.path.join("output", pid))
        df.to_csv(os.path.join("output", pid, "interactions.csv"))
        print(df.head(), end="\n")