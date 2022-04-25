import subprocess

subprocess.call("python -m pytest test_sail_safe_functions -sv", shell=True, cwd="sail-safe-functions-test/sail_safe_functions_test")
