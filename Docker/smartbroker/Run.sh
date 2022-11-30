#!/bin/bash
imageName=smartbroker

PrintHelp() {
    echo ""
    echo "Usage: $0 -d"
    echo -e "\t-d Run docker container in dev mode"
    exit 1 # Exit script after printing help
}

# Parse the input parameters
while getopts "d opt:" opt; do
    case "$opt" in
    d) mode="dev" ;;
    ?) PrintHelp ;;
    esac
done

# Check if docker is installed
docker --version
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error docker does not exist"
    exit $retVal
fi

# Check if the image exists
imageNameFound=$(docker image ls --filter reference=$imageName --format {{.Repository}})
echo "$imageNameFound"
if [ "$imageNameFound" == "$imageName" ]
then
    echo "Docker image exists"
else
    echo "!!! Docker image not found !!!"
    exit 1
fi

echo "Running $imageName in $mode mode"

if [ "$mode" == "dev" ]
then
    echo "Running in dev mode"
    mountOption=$(pwd)/../../:/app/datascience
    detach=it
else
    echo "Running in prod mode"
    # Create a folder to hold all the Binaries
    mkdir -p "$imageName"_dir
    # Copy the binaries to the folder
    cp vm_initializer.py "$imageName"_dir/
    cp InitializationVector.json "$imageName"_dir/

    detach=it
    mountOption=$(pwd)/"$imageName"_dir:/app
fi

# Run the docker container
docker run \
-$detach \
-p 8000:8001 \
-p 9090:9091 \
--env MODE=$mode \
-v $mountOption \
-v $(pwd)/certs:/etc/nginx/certs \
$imageName
