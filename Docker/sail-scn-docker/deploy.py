# docker run -p hostPort:containerPort imageName


# docker run --it --entrypoint=bash pklehre/niso2020-lab2-msc


import os
import subprocess
import sys


# usage example
# export PATH_FILE_GIT_TOKEN
# python deploy.py BOARD-2078-B BOARD-2078
def run(command: str):
    print(command)
    subprocess.call(command)


if __name__ == "__main__":
    # remove containers

    # remove images

    # name_data_federation: str = sys.argv[1]
    path_dir_dataset = os.environ["PATH_DIR_DATASET"]
    path_dir_public_key_zeromq = os.environ["PATH_DIR_PUBLIC_KEY_ZEROMQ"]
    path_file_private_key_zeromq = os.environ["PATH_FILE_PRIVATE_KEY_ZEROMQ_SERVER"]

    command: str = "docker run"
    command += " -it"
    command += f" --mount src={path_dir_public_key_zeromq},target=/app/RPCLib/public_keys/,type=bind"
    command += (
        f" --mount src={path_file_private_key_zeromq},target=/app/RPCLib/private_keys/server.key_secret,type=bind"
    )
    command += f" --mount src={path_dir_dataset},target=/data/,type=bind"

    command += " -e PATH_DIR_PUBLIC_KEY_ZEROMQ=/app/RPCLib/public_keys/"
    command += " -e PATH_FILE_PRIVATE_KEY_ZEROMQ_SERVER=/app/RPCLib/private_keys/server.key_secret"

    command += " -e PATH_DIR_DATASET=/data/"

    command += " -p 5010:5010"
    command += " --entrypoint=/entrypoint_participant.sh"
    command += " sail/im_scn ."
    run(command)


# export PATH_DIR_PUBLIC_KEY_ZEROMQ="/c/key/public_key_zeromq"
# export PATH_FILE_PRIVATE_KEY_ZEROMQ_SERVER="/c/key/private_key_zeromq/server.key_secret"

# /app/RPCLib/public_keys/#
