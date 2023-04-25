import subprocess

subprocess.call(
    "python -m pytest sail_safe_functions/test/ -m active -sv",
    shell=True,
    cwd="sail-safe-functions",
)


subprocess.call(
    "nohup python main_test.py",
    shell=True,
    cwd="sail-aggregator-fastapi",
)

subprocess.call(
    "python-m pytest test_user_client -m active",
    shell=True,
    cwd="sail-user-client",
)
