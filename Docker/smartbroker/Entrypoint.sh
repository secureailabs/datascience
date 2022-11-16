#!/bin/bash
set -e
imageName=smartbroker

cd /app || exit

# Start the nginx server
nginx -g 'daemon off;' 2>&1 | tee /app/nginx.log &

# vm_initializer will download the package.tar.gz and InitializationVector.json
# if they are not already present on the file system.
# Forcing a zero exit status as the api server is killed from within and there is no graceful way to do this.
if [ "$MODE" == "dev" ]; then
    echo "Running in dev mode"
    # Move the InitializerVector to the Binary folder
    reload=--reload
    cp SmartBroker/Docker/smartbroker/InitializationVector.json SmartBroker/
else
    python3 vm_initializer.py || true
    retVal=$?
    if [ $retVal -ne 0 ]; then
        exit $retVal
    fi

    # Unpack the tar package
    tar -xf package.tar.gz

    # Move the InitializerVector to the Binary folder
    mv InitializationVector.json SmartBroker/
fi

# Start the Public API Server
cd SmartBroker
python3 build/install.py

cd fastapi
uvicorn main:app --host 0.0.0.0 --port 8000 $reload

# To keep the container running
tail -f /dev/null
