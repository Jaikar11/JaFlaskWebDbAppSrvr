#!/bin/bash
cd ~/repos
python3 -m venv venv
source venv/bin/activate
cd JaFlaskWebDbAppSrvr/
FILE1="log.txt"
FILE2="ipaddress.txt"
if [ ! -f "$FILE1" ]; then
    touch "$FILE1"
    echo "$FILE1 created."
fi
if [ ! -f "$FILE2" ]; then
    touch "$FILE2"
    echo "$FILE2 created."
fi
chmod 777 "$FILE1"
chmod 777 "$FILE2"
hostname -I | awk '{print $1}' > ./ipaddress.txt
echo "localhost:3306" > ./rds_endpoint.txt
sudo pip3 install -r requirements.txt
FLASK_APP=App.app.py flask run --host='0.0.0.0' --port=5000
#FLASK_APP=App.app.py flask run --host='0.0.0.0' --port=5000 >>log.txt 2>&1 &
