#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = {}
with open("pali/__init__.py") as fp:
    exec(fp.read(), version)

setuptools.setup(
    name="pali",
    version=version['__version__'],
    author="Vipin Sharma",
    author_email="sh.vipin@gmail.com",
    description="A simple ThreadPool library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitvipin/pali",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
