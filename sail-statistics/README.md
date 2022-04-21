# Secure AI Labs

## Create your virtual environment
## Install package
- Install Python 3.8 and add python to PATH
- Clone datascience Repo
- Create a virtual environment: `python -m venv <name_venv>`
- Starting the name with "venv" will have it ignored via the gitignorefile 
- Activate your Virtual env (venv): `.\<name_venv>\Scripts\activate` OR `source <name_venv>\bin\activate`
- Navigate to the sail-statistics root
- Install package on your Virtual env (venv): `pip install .`

## Run Test package
- Clone sailtap Repo
- Create sailtap repo virtual env
- Navigate to sailtap root
- Install sailtap dependences `pip install -r requirements.txt`
- Clone datascience Repo
- Navigate to the sail-statistics root
- Install package `pip install .`
- Navigate back to sailtap root
- run tests with `python -m pytest test_sail_safe_functions -sv`

## Uninstall package
pip remove sail-statistics

## Deactivate your Virtual Env (venv)
- Exit from your Virtual Env `deactivate`