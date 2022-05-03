
[![.github/workflows/linter.yml](https://github.com/secureailabs/datascience/actions/workflows/linter.yml/badge.svg)](https://github.com/secureailabs/datascience/actions/workflows/linter.yml)
# Secure AI Labs Datasciece repo

## Overview
The repository contains 3 python packages 
- `sail-safe-functions` contains only "Scripts" that get converted into safe functions
- `sail-safe-functions-federate` functions that we use to federate out safe functions, these should eventually end up in the ochestrator
- `sail-safe-functions-test` contains the unit test 

- the `build` folder contains python configuration scripts for the repo
- the `config` folder contains dependency management files  `ie: requirements.txt`
- the `docs` folder contains the documentation that we generate and is published on github pages


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
*`Dependency Requirements are listed in config/requirements/*.txt`*

## Run Test package
- Run `python run_tests.py`

## Generate Documentation
- Run `python build/documentation.py`

## Deactivate your Virtual Env (venv)
- Exit from your Virtual Env `deactivate`
