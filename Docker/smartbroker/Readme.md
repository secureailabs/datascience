## Build docker image
```
docker build . -t smartbroker
```

## Run docker image
```
./Run.sh -d
```

The -d option will run the docker image in dev mode. This will:
1. mount the local directory instead of the docker container waiting for a package
2. reload the fastapi server on file change automatically (no need to restart the server)
3. run the smartbroker container in interactive mode instead of detached mode (so you can see the logs)
