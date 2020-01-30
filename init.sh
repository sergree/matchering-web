#!/bin/bash

export SECRET_KEY=`date +%s|sha256sum|base64|head -c 50`

python3 manage.py flush --no-input
python3 manage.py makemigrations mgw_back
python3 manage.py migrate

# https://docs.docker.com/config/containers/multi-service_container/
supervisord -c /usr/src/app/supervisord.conf
