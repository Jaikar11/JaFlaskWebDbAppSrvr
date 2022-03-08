#!/bin/bash
sudo curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
cd /home/ec2-user/
python3 -m venv venv
source venv/bin/activate
sudo pip3 install flask
cd JaFlaskWebDbApp/
sudo pip3 install -r requirements.txt
FLASK_APP=App.app.py flask run --host='0.0.0.0' --port=5000