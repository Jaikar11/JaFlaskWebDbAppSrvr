#!/bin/bash
python3 -m venv venv
source venv/bin/activate
cd /home/ec2-user/
ls
cd /home/ec2-user/JaFlaskWebDbApp
sudo pip install flask
sudo pip install -r requirements.txt
FLASK_APP=App.app.py flask run --host='0.0.0.0' --port=5000