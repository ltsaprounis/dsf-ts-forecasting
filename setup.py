__author__ = ["author name"]

from setuptools import setup, find_packages

setup(
    name="dsf_utils",
    version="0.0.0",
    packages=find_packages(),
    description="package description",
    author="author name",
    install_requires=[
        "sktime",
    ],
)
