#!/bin/bash
SERVICE="flask"   
DIRNAME="JaFlaskWebDbAppSrvr"

if pgrep -x "$SERVICE" >/dev/null   // Check if Flask is running. If running stop the flask process
then
    echo "$SERVICE is running"
    ps aux | grep -i flask | grep -v grep| awk {'print $2'} | sudo xargs kill // Stop flask
else
    echo "$SERVICE is not running" 
fi

if [[ -d "$DIRNAME"  ]]     
then 
  echo "$DIRNAME - Directory exits"
  sudo rm -rf /home/ec2-user/JaFlaskWebDbAppSrvr
  echo "$DIRNAME - Directory is cleared for reinstall"
else
 echo  "$DIRNAME - Directory doesn't exist"	
fi
