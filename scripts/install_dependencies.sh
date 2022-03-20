#!/bin/bash
python3 -m venv venv
source venv/bin/activate
cd /home/ec2-user/
sudo aws s3 cp s3://ja-day12-config/rds_endpoint.txt rds_endpoint.txt
cd /home/ec2-user/JaFlaskWebDbAppSrvr
sudo touch ./templates/ipaddress.txt
chmod 777 ./templates/ipaddress.txt
sudo curl checkip.amazonaws.com >> ./templates/ipaddress.txt
sudo pip3 install flask
sudo pip3 install -r requirements.txt
