import subprocess

subprocess.run(["pip", "uninstall", "sail-safe-functions", "-y"])
subprocess.run(["pip", "uninstall", "sail-safe-functions-orchestrator", "-y"])
subprocess.run(["pip", "uninstall", "sail-safe-functions-test", "-y"])
