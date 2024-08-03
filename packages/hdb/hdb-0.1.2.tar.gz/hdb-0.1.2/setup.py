import hdb
from setuptools import setup, find_packages

setup(
    name="hdb",
    version="0.1.2",
    author="Chris Varga",
    author_email="",
    description="HobbitDB - persistent Python dictionaries",
    long_description=hdb.__doc__,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="hdb hobbit database persistent dictionary json",
)
