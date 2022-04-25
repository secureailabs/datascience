# Secure AI Labs Datasciece repo

## Overview
The repository contains 3 python packages 
- "sail-safe-functions" contains only "Scripts" that get converted into safe functions
- "sail-safe-functions-federate" functions that we use to federate out safe functions, these should eventually end up in the ochestrator
- "sail-safe-functions-test" contains the unit test 

Although each of these has their own requirements.txt they should never conflict.

- the docs folder also contains the documentation that we generate and is published on github pages

## Create virtual environment
- Install Python 3.8
- Clone datascience Repo
- Create a virtual environment: `py -3.8 -m venv venv38_sail`

## Activate virtual environment
- Activate a virtual environment: `source venv38_sail/Scripts/activate`

## Install repositories
- Run `python install.py`

## Run Test package
- Run `python run_tests.py`

## Generate Documentation
- Run `python documentation.py`

## Deactivate your Virtual Env (venv)
- Exit from your Virtual Env `deactivate`