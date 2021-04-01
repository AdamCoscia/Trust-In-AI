hostname=$(python -c "import json; print(json.load(open('redis.json'))['hostname'])")
password=$(python -c "import json; print(json.load(open('redis.json'))['password'])")
port=$(python -c "import json; print(json.load(open('redis.json'))['port'])")
rdcli -h $hostname -a $password -p $port