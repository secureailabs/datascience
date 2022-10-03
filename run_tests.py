import subprocess

subprocess.call(
    "python -m pytest sail_test/ -m active -sv",
    shell=True,
    cwd="sail_test",
)
