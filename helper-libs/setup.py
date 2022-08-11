from setuptools import find_packages, setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="helper-libs",
    version="0.0.1",
    packages=find_packages(),
    package_data={},
    python_requires=">=3.5",
    author="Jaap Oosterbroek, Adam Hall",
    author_email="jaap@secureailabs.com",
    description="A set of helper libraries to be used in the sail ecosystem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nowhere.not",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: SAIL :: Propritary",
        "Operating System :: OS Independent",
    ],
)
