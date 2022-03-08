#!/bin/bash
python3 -m venv venv
source venv/bin/activate
cd /home/ec2-user/
echo $(ls)
cd /home/ec2-user/JaFlaskWebDbAppSrvr
sudo pip install flask
sudo pip install -r requirements.txt
FLASK_APP=App.app.py flask run --host='0.0.0.0' --port=5000