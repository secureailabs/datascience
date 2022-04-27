import subprocess

subprocess.call(
    "python -m pytest sail_safe_functions_test/ -m active -sv",
    shell=True,
    cwd="sail-safe-functions-test",
)
