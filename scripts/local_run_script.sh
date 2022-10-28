#!/bin/bash
source venv/bin/activate
cd ~/JaFlaskWebDbAppSrvr
touch log.txt
chmod 777 log.txt
sudo touch ./ipaddress.txt
sudo chmod 777 ./ipaddress.txt
hostname -I | awk '{print $1}' > ./ipaddress.txt
sudo pip3 install flask
sudo pip3 install -r requirements.txt
FLASK_APP=App.app.py flask run --host='0.0.0.0' --port=5000
#FLASK_APP=App.app.py flask run --host='0.0.0.0' --port=5000 >>log.txt 2>&1 &

