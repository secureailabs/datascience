import subprocess

subprocess.call(
    "python -m pytest sail_safe_functions/test/ -m active -sv",
    shell=True,
    cwd="sail-safe-functions",
)
