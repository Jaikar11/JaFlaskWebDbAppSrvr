#!/bin/bash
cd /home/ec2-user/JaFlaskWebDbAppSrvr
FLASK_APP=App.app.py flask run --host='0.0.0.0' --port=5000