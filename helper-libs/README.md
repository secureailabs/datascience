# Helper Library

This library is experimental and intended to support the execution of safe functions. It is set up in two 'seperate' spaces:

- The scn_side lib holds functionality to be installed on the scn and to be importable to a safe function runtime environment
- The shared lib holds functionality to be made available to both the orchestrator and the scn runtime environment

in order to use this lib you will need to reinstall the datascience library in your runtime environment. 

`python build/install.py`