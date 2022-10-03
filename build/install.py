import subprocess

subprocess.run(["pip", "install", "-r", "config/requirements/internal.txt"])
subprocess.run(["pip", "install", "-e", "sail_scn_lib"])
subprocess.run(["pip", "install", "-e", "sail_orchestrator_lib"])
subprocess.run(["pip", "install", "-e", "sail_test"])
subprocess.run(["pip", "install", "-e", "helper-libs"])
