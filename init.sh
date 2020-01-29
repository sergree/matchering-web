#!/bin/bash
# Run this script using "source init.sh"

if [ -z ${SECRET_KEY+x} ]; then
    RND_VALUE=`date +%s|sha256sum|base64|head -c 50`
    export SECRET_KEY="$RND_VALUE"
    echo "export SECRET_KEY="$RND_VALUE"" >> ~/.bashrc
fi

python3 manage.py makemigrations mgw_back
python3 manage.py migrate

# https://docs.docker.com/config/containers/multi-service_container/
set -m
python3 manage.py runserver 0:8360 &
python3 manage.py rqworker default 
fg %1
