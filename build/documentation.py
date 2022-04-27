import os
import shutil
import subprocess

script_dir = os.path.dirname(os.path.realpath(__file__))
print(f"Script Directory: {script_dir}")
os.chdir(script_dir)

if os.path.isdir("../docs"):
    shutil.rmtree("../docs")

subprocess.run(["pdoc", "sail_safe_functions", "--html", "-o", "../docs"])
subprocess.run(["pdoc", "sail_safe_functions_orchestrator", "--html", "-o", "../docs"])
subprocess.run(["pdoc", "sail_safe_functions_test", "--html", "-o", "../docs"])
shutil.copyfile("index.html.bak", "../docs/index.html")