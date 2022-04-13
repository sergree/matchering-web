#!/bin/bash

# Matchering WEB - Handy Matchering 2.0 Containerized Web Application
# Copyright (C) 2016-2022 Sergree

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

file="./.secret_key"
if [ -f "$file" ]
then
    echo "Using an existing SECRET_KEY..."
else
    echo "Generating a new SECRET_KEY..."
    echo `date +%s|sha256sum|base64|head -c 50` > "$file"
fi

python3 manage.py makemigrations mgw_back
python3 manage.py migrate

# https://docs.docker.com/config/containers/multi-service_container/
supervisord -c /app/supervisord.conf
