#!/bin/bash
python3 -m venv venv
source venv/bin/activate
cd /home/ec2-user/
aws s3 cp s3://ja-day12-config/rds_endpoint.txt
cd /home/ec2-user/JaFlaskWebDbAppSrvr
sudo pip3 install flask
sudo pip3 install -r requirements.txt
