#!/bin/bash

SERVICE="flask"
if pgrep -x "$SERVICE" >/dev/null
then
    echo "$SERVICE is running"
    exit 0
else
    echo "$SERVICE is not running"
    exit 123
fi
