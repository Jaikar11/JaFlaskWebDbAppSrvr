#!/bin/bash
python3 -m venv venv
source venv/bin/activate
cd /home/ec2-user/
echo $(ls)
cd /home/ec2-user/JaFlaskWebDbAppSrvr
sudo pip3 install flask
sudo pip3 install -r requirements.txt
FLASK_APP=App.app.py flask run --host='0.0.0.0' --port=5000