#!/bin/bash
sudo service httpd stop
source register_with_elb.sh
source venv/bin/activate
cd /home/ec2-user/JaFlaskWebDbAppSrvr
touch log.txt
chmod 777 log.txt
FLASK_APP=App.app.py flask run --host='0.0.0.0' --port=5000 >>log.txt 2>&1 &