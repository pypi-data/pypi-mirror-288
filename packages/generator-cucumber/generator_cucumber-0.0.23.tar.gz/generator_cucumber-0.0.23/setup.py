#!/usr/bin/env python
from setuptools import setup, find_packages

exec(open("generator_cucumber/_version.py").read())

setup(
  name='generator_cucumber',
  version=__version__,
  packages=find_packages(),
)