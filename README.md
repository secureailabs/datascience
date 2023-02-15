
[![.github/workflows/linter.yml](https://github.com/secureailabs/datascience/actions/workflows/linter.yml/badge.svg)](https://github.com/secureailabs/datascience/actions/workflows/linter.yml)
# Secure AI Labs Datasciece repo

## Overview
The repository contains 5 python packages
- `sail-aggregator-fastapi` contains all code relating to running an aggregator scn service.
- `sail_core` contains all core functionality needed to run in other packages. This includes and implementation manager and common tools.
- `sail-participant-zeromq` contains all code needed to run a local copy of a `sail_zeromq` server. These act as data holding nodes.
- `sail-safe-functions` contains only "Scripts" that get converted into safe functions. This includes both scripts which are held on SCNs and an aggregator SCN. This also includes all tests for safe funcitons.
- `sail-user-client` contains all the code used by a researcher to interact with a deployed platform. This contains two submodules. `sail_aggregator_client` contains internally facing packages which abstract away the majority of fastapi interactions from the user. `sail_user_client` is the customer facing api which interacts with `sail_aggregator_client` and facilitates the user experience in the sail platform.

- the `build` folder contains python configuration scripts for the repo
- the `config` folder contains dependency management files  `ie: requirements.txt`
- the `notebooks` directory contains a list of code examples
- the `docs` folder contains the documentation that we generate and is published on github pages

An up to date list of functionality that is available for use is held [here](https://fluffy-couscous-a7e264fe.pages.github.io/)



## Create virtual environment
- Install Python 3.8
- Clone datascience Repo
- [Create a virtual environment](https://docs.python.org/3/library/venv.html) \
`example in linux : python3 -m venv venv38_sail` \
`example in Windows: python -m venv c:\path\to\venv38_sail`

## Activate virtual environment
- Activate virtual environment on Windows: `venv38_sail\Scripts\activate`
- Activate virtual environment on Linux `source venv38_sail/bin/activate`

## Install all Dependencies for local development
- Run `python build/install.py` \

## Run Test package
- Run `python run_tests.py`

## Generate Documentation
- Run `python build/documentation.py`

## Deactivate your Virtual Env (venv)
- Exit from your Virtual Env `deactivate`

## running integration test - localhost - FHIR

Set environment variables:
Or define them in your bashrc file
This is a bit of a mess but an example there is an example for r4sep2019_fhirv1_60_3 in DOCKER/smartbroker/InitializationVector.json
NOTE!!! the IV_FILEPATH evironment veriable is specific to the notebook you are running, SET it apropriately!
- Run `export IV_FILEPATH=""`

- Run `export PATH_DIR_DATASET=""`
- Run `export PATH_DIR_PUBLIC_KEY_ZEROMQ=""`
- Run `export PATH_FILE_PRIVATE_KEY_ZEROMQ_CLIENT=""`
- Run `export PATH_FILE_PRIVATE_KEY_ZEROMQ_SERVER=""`

terminal 1
- Run `cd sail-participant-zeromq`
- Run `python server.py 5010`
terminal 2
- Run `cd sail-aggregator-fastapi`
- Run `uvicorn aggregator_fastapi:app --host 0.0.0.0 --port 8000`
terminal 3
- Run `cd notebooks`
- Run `jupyter notebook`
- Select `platform_localhost_fhir.ipynb`
- Run every cell exactly once in sequence