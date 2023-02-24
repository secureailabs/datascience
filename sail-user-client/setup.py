from setuptools import find_packages, setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="sail-user-client",
    version="1.0.1",
    packages=(find_packages()),
    package_data={},
    python_requires=">=3.5",
    author="Adam Hall",
    author_email="adam.hall@secureailabs.com",
    description="THe primary means by which a researcher interacts with the SAIL platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nowhere.not",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: SAIL :: Propritary",
        "Operating System :: OS Independent",
    ],
)
