#!/bin/bash
#set -x

#cd ~/Ja-Repos/JaFlaskWebDbAppSrvr/Local-run
python3 --version
if [[ $? -eq 0 ]];then
    echo "Python 3 is installed"
else
    echo "ERROR: Python 3 is available"
    exit 1 # terminate as Python3 is not available
fi

pip3 --version

if [[ $? -ne 0 ]];then
    apt update
    apt-get install -y python3-pip python3-dev
    pip3 --version
    if [[ $? -ne 0 ]];then
        echo "ERROR: Python 3 pip is not installed / available"
        exit 1 # terminate as pip3 is not available
    else
        echo "Python pip3 is installed now"
    fi
else
    echo "Python pip3 is available"
fi

virtualenv --version
if [[ $? -ne 0 ]];then
    apt-get install -y python3-virtualenv
    virtualenv --version
    if [[ $? -ne 0 ]];then
        echo "ERROR: virtualenv pip is not installed / available"
        exit 1 # terminate as virtualenv is not available
    else
        echo "Python virtualenv is installed now"
    fi
else
    echo "virtualenv is available"
fi

python3 -m virtualenv venv
source venv/bin/activate
FILE1="log.txt"
FILE2="ipaddress.txt"
if [ ! -f "$FILE1" ]; then
    touch "$FILE1"
    echo "$FILE1 created."
fi
if [ ! -f "$FILE2" ]; then
    touch "$FILE2"
    echo "$FILE2 created."
fi
chmod 777 "$FILE1"
chmod 777 "$FILE2"
hostname -I | awk '{print $1}' > ./ipaddress.txt
echo "172.31.112.44" > ./rds_endpoint.txt
pip3 install -r requirements.txt
FLASK_APP=App.app.py flask run --host='0.0.0.0' --port=5000
#FLASK_APP=App.app.py flask run --host='0.0.0.0' --port=5000 >>log.txt 2>&1 &
