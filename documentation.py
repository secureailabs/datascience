import shutil
import subprocess

shutil.rmtree("docs")
subprocess.call("pip install pdoc3")
subprocess.call("pdoc sail_safe_functions --html -o docs")
subprocess.call("pdoc sail_safe_functions_orchestrator --html -o docs")
subprocess.call("pdoc sail_safe_functions_test --html -o docs")
