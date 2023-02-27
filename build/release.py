#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import subprocess
from typing import Dict, List, Optional

from github import Github


def run_command(command: str, check=True, path: Optional[str] = None):
    if path is None:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, check=check)
    else:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, check=check, cwd=path)
    return result.stdout.decode("utf-8").strip()


def get_repo_info():
    repo_remote = run_command("git config --get remote.origin.url")

    if not repo_remote:
        raise RuntimeError("Local path not a git repository")

    repo_name = re.sub(r"\.git$", "", os.path.basename(repo_remote))
    repo_owner = run_command("git config --get user.name")

    repo_current_branch = run_command("git rev-parse --abbrev-ref HEAD")
    repo_latest_tag = run_command("git describe --tags --abbrev=0")

    repo_info = {}
    repo_info["repo_remote"] = repo_remote
    repo_info["repo_name"] = repo_name
    repo_info["repo_owner"] = repo_owner
    repo_info["repo_current_branch"] = repo_current_branch
    repo_info["repo_latest_tag"] = repo_latest_tag

    print(repo_info)
    return repo_info


def check_is_most_recent():
    pass


def get_version(list_name_package: List[str]):
    list_name_module = [name_package.replace("-", "_") for name_package in list_name_package]
    list_version = []
    for name_package, name_module in zip(list_name_package, list_name_module):
        with open(os.path.join(name_package, name_module, "__init__.py")) as file:
            version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)
            list_version.append(version)
    if 1 < len(set(list_version)):
        raise RuntimeError(f"multiple versions in repository: {str(list_version)}")
    return list_version[0]


def build_wheels(list_name_package: List[str]) -> Dict[str, str]:
    dict_wheel = {}
    for name_package in list_name_package:
        print(f"building package: {name_package}")
        run_command("python setup.py bdist_wheel", path=name_package)
        path_dir_dist = os.path.join(name_package, "dist")
        for name_file in os.listdir(path_dir_dist):
            path_file_wheel = os.path.abspath(os.path.join(name_package, "dist", name_file))
            dict_wheel[name_file] = path_file_wheel
    return dict_wheel


def build_upload(release, dict_wheel: Dict[str, str]):
    print(type(release))
    for name_wheel, path_file_wheel in dict_wheel.items():
        print("uploading_wheel")
        print(name_wheel)
        print(path_file_wheel)
        with open(path_file_wheel, "rb") as file:
            bytes_wheel = file.read()
        release.upload_asset_from_memory(bytes_wheel, len(bytes_wheel), name_wheel)


def build_clean(list_name_package: List[str]) -> None:
    for name_package in list_name_package:
        path_dir_build = os.path.join(name_package, "build")
        path_dir_dist = os.path.join(name_package, "dist")
        shutil.rmtree(path_dir_build)
        shutil.rmtree(path_dir_dist)


if __name__ == "__main__":
    # Config of script
    list_name_package = ["sail-core", "sail-safe-functions"]
    name_branch = "main"
    dict_tagger = {"name": "Jaap Oosterbroek", "email": "jaap@secureailabs.com", "date": "2011-06-17T14:53:35-07:00"}
    # End config of script

    if "PATH_FILE_GIT_TOKEN" not in os.environ:
        raise RuntimeError("Environment variable not set: PATH_FILE_GIT_TOKEN")
    path_file_git_token = os.environ["PATH_FILE_GIT_TOKEN"]
    with open(path_file_git_token, "r") as file:
        access_token = file.read()

    # check if git repo
    repo_info = get_repo_info()

    check_is_most_recent()
    version_tag = get_version(list_name_package)

    print(f"Building Release {version_tag} from branch {name_branch} now.")

    # create tag via git commands
    # shell(f"git tag {str(new_version)}")
    # shell(f"git push origin {str(new_version)}")

    github = Github(access_token)
    repository = github.get_user("secureailabs").get_repo(repo_info["repo_name"])
    tag_message = "new release"
    release_name = version_tag
    release_message = "greatest release message"
    commit_object: str = repository.get_branch("main").commit.sha
    from github import InputGitAuthor

    tagger = InputGitAuthor(dict_tagger["name"], dict_tagger["email"])
    is_draft = True

    print(repository.get_branch("main").commit.sha)
    print(repository.name)
    for release in repository.get_releases():
        if release.tag_name == version_tag:
            raise RuntimeError("tag exists")

    tag_object = repository.create_git_tag(
        version_tag,
        tag_message,
        object=commit_object,
        type="commit",
        tagger=tagger,
    )
    print(tag_object)
    print(tag_object.object)
    print(tag_object.sha)
    print(tag_object.update())

    git_reference = repository.create_git_ref(f"refs/tags/{version_tag}", tag_object.sha)

    release = repository.create_git_release(
        tag_object.sha,
        release_name,
        release_message,
        is_draft,
        False,
        target_commitish=commit_object,
    )
    print(release)
    print(release.id)

    # for release in repository.get_releases():
    #     print(release.tag_name)
    #     release_id = print(release.id)
    # print("latests")
    # release = repository.get_latest_release()
    # print(release.tag_name)
    # print(release.id)
    # print("upload")
    # release = repository.get_releases()[0]
    # release = repository.get_release("v1.0.3")

    # build windows wheel
    # wheel_name = f"{dist}-{version}-{python.version}-{os_platform}.whl"

    dict_wheel = build_wheels(list_name_package)
    build_upload(release, dict_wheel)
    build_clean(list_name_package)

    # create installable zip
    # git archive --format=zip -v --output=../<reponame>.zip --worktree-attributes HEAD

    print("All done.")
