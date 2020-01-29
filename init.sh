#!/bin/bash

# Run it using "source init.sh"

if [ -z ${SECRET_KEY+x} ]; then
    RND_VALUE=`date +%s|sha256sum|base64|head -c 50`
    export SECRET_KEY="$RND_VALUE"
    echo "export SECRET_KEY="$RND_VALUE"" >> ~/.bashrc
fi

# ??? cd /vagrant/matchering_web
# python3 manage.py makemigrations mgw_back
# python3 manage.py migrate
# python3 manage.py runserver 0:8360
# uvicorn matchering_web.asgi:application --host 0.0.0.0 --port 8360
# python3 manage.py rqworker default
