import os
import subprocess
import sys


# usage example
# export PATH_FILE_GIT_TOKEN
# python build.py BOARD-2078-B BOARD-2078
def run(command: str):
    subprocess.call(command)


if __name__ == "__main__":
    # config
    path_file_git_token = os.environ["PATH_FILE_GIT_TOKEN"]
    with open(path_file_git_token, "r") as file:
        git_personal_token = file.read()

    # remove containers

    # remove images

    branch_datascience: str = sys.argv[1]
    branch_engineering: str = sys.argv[2]

    command: str = "docker build -f df_scn"
    command += f" --build-arg git_personal_token={git_personal_token}"
    command += f" --build-arg branch_datascience={branch_datascience}"
    command += f" --build-arg branch_engineering={branch_engineering}"
    command += f" -t sail/im_scn ."
    run(command)
