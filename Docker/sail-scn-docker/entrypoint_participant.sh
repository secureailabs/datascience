#!/bin/bash


# Start the nginx server
#nginx -g 'daemon off;' 2>&1 | tee /app/nginx.log &

# Start the Public API Server
/bin/python3.8 /datascience/sail-participant-zeromq/server.py 5010

