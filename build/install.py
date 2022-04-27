import subprocess

subprocess.run(["pip", "install", "-r", "config/requirements/internal.txt"])
subprocess.run(["pip", "install", "-e", "sail-safe-functions"])
subprocess.run(["pip", "install", "-e", "sail-safe-functions-orchestrator"])
subprocess.run(["pip", "install", "-e", "sail-safe-functions-test"])
