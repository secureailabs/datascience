import re

from setuptools import find_packages, setup

version = ""
with open("sail_core/__init__.py") as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

requirements = []
with open("requirements.txt") as file:
    requirements = file.read().splitlines()

with open("README.md", "r") as file:
    long_description = file.read()

# find_packages(exclude=("test",)),

setup(
    name="sail-core",
    version=version,
    install_requires=requirements,
    packages=find_packages(),
    package_data={},
    python_requires="==3.8.10",
    author="Jaap Oosterbroek",
    author_email="jaap@secureailabs.com",
    description="A basic set of functions, classes and interfaces for sail-libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nowhere.not",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: SAIL :: Propritary",
        "Operating System :: OS Independent",
    ],
)
