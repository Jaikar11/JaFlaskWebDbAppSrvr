#!/bin/bash
python3 -m venv venv
source venv/bin/activate
cd /home/ec2-user/
cd /home/ec2-user/JaFlaskWebDbAppSrvr
source scripts/deregister_from_elb.sh
sudo pip3 install flask
sudo pip3 install -r requirements.txt
