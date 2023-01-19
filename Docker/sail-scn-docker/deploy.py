docker run -p hostPort:containerPort imageName



    # docker run --it --entrypoint=bash pklehre/niso2020-lab2-msc


import os
import subprocess
import sys


# usage example
# export PATH_FILE_GIT_TOKEN
# python deploy.py BOARD-2078-B BOARD-2078
def run(command: str):
    subprocess.call(command)


if __name__ == "__main__":
    # remove containers

    # remove images

    name_data_federation: str = sys.argv[1]

    command: str = "docker run"

    command += f" -t sail/im_scn ."
    command += f" -p hostPort:containerPort"

    run(command)
