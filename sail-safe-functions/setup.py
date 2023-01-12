from setuptools import find_packages, setup

requirements = []
with open("requirements.txt") as file:
    requirements = file.read().splitlines()

with open("README.md", "r") as file:
    long_description = file.read()

# find_packages(exclude=("test",)),

setup(
    name="sail-safe-functions",
    version="1.0.1",
    install_requires=requirements,
    packages=find_packages(),
    package_data={},
    python_requires="==3.8.10",
    author="Jaap Oosterbroek",
    author_email="jaap@secureailabs.com",
    description="A set of safe functions to be used on the sail platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nowhere.not",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: SAIL :: Propritary",
        "Operating System :: OS Independent",
    ],
)
