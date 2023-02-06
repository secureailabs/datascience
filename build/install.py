import subprocess

subprocess.run(["pip", "install", "-e", "sail-core"])
subprocess.run(["pip", "install", "-e", "sail-safe-functions"])
subprocess.run(["pip", "install", "-e", "sail-aggregator-fastapi"])
subprocess.run(["pip", "install", "-e", "sail-participant-zeromq"])
