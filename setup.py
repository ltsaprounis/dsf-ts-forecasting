__author__ = ["Leonidas Tsaprounis"]

from setuptools import setup, find_packages

setup(
    name="dsf_utils",
    version="0.0.0",
    packages=find_packages(),
    description="utility functions and classes for the DSF presentation",
    author="Leonidas Tsaprounis",
    install_requires=[
        "sktime",
    ],
)
