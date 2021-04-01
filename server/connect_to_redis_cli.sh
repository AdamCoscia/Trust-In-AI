host=$(python -c "import json; print(json.load(open('redis.json'))['host'])")
port=$(python -c "import json; print(json.load(open('redis.json'))['port'])")
password=$(python -c "import json; print(json.load(open('redis.json'))['password'])")
rdcli -h $host -a $password -p $port