__author__ = ["author name"]

from setuptools import setup, find_packages

setup(
    name="examplepackage",
    version="x.x",
    packages=find_packages(),
    description="package description",
    author="author name",
    install_requires=[
        "numpy>=1.0",
        "pandas==1.0",
    ],
)
