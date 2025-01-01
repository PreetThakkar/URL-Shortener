#!/bin/bash

# Config variables
WORK_DIR="/home/preet/Workspace/URL-Shortener"
ENV_DIR="/opt/python-envs/url-env" # Python env path

# Constants
BACKEND_DIR=$WORK_DIR/backend
FRONTEND_DIR=$WORK_DIR/frontend
SERVER_PID=$BACKEND_DIR/server.pid
CLIENT_PID=$FRONTEND_DIR/server.pid

# Backend
cd $BACKEND_DIR
source $ENV_DIR/bin/activate
if [ -s "$SERVER_PID" ]; then
    echo "Previous backend process terminated"
    sudo kill -9 "$(cat $SERVER_PID)"
fi
SCRIPT_NAME=/api gunicorn app:app -w 3 --worker-class=gevent -b localhost:5000 > /dev/null 2>&1 &
echo $! > $SERVER_PID
echo "Backend started with PID: $(cat $SERVER_PID)"

# Frontend
cd $FRONTEND_DIR
npm i
if [ -s "$CLIEND_PID" ]; then
    echo "Previous frontend process terminated"
    sudo kill -9 "$(cat $CLIEND_PID)"
fi
npm start > /dev/null 2>&1 &
echo $! > $CLIENT_PID
echo "Frontend started with PID: $(cat $CLIEND_PID)"