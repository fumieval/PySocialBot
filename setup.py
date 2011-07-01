#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="PySocialBot",
    version="0.2.5",
    description="Advanced Bot Framework",
    license="BSD",
    keywords="Bot Twitter",
    url="http://botis.org/wiki/PySocialBot",
    packages=find_packages(exclude=['examples']),
    include_package_data=True,
)