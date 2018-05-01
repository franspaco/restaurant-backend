#!/bin/bash

cd

server_dir="restaurant-backend"

if [ ! -d "$server_dir" ]; then
    git clone https://github.com/franspaco/restaurant-backend.git
    cd restaurant-backend
else
    cd restaurant-backend
    git pull origin master
fi


#required because python
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# flask
export FLASK_APP=project

# defaults
export MONGO_HOST=${MONGO_HOST:-"localhost"}
export MONGO_PORT=${MONGO_PORT:-"27017"}
export HOST=${HOST:-"0.0.0.0"}
export PORT=${PORT:-"80"}

flask run --port $PORT --host $HOST