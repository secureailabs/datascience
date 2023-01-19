#!/bin/bash


# Start the nginx server
#nginx -g 'daemon off;' 2>&1 | tee /app/nginx.log &

# Start the Public API Server
export PATH_DIR_PUBLIC_KEY_ZEROMQ="/app/RPCLib/public_keys/"
export PATH_FILE_PRIVATE_KEY_ZEROMQ_CLIENT="/app/RPCLib/private_keys/client.key_secret"
export PATH_DIR_DATASET="/data/"

/bin/python3.8 /datascience/sail-participant-zeromq/server.py 5010

