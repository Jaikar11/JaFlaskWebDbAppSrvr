#!/bin/bash
source venv/bin/activate
cd /home/ec2-user/JaFlaskWebDbAppSrvr
FLASK_APP=App.app.py flask run --host='0.0.0.0' --port=5000 >>log.txt 2>&1 &