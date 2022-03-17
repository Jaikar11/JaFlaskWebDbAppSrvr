#!/bin/bash
python3 -m venv venv
source venv/bin/activate
cd /home/ec2-user/
cd /home/ec2-user/JaFlaskWebDbAppSrvr
pip3 install flask --user
sudo pip3 install -r requirements.txt
