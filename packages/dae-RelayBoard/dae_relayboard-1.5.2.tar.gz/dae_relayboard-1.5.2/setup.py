#!/usr/bin/env python

from distutils.core import setup

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="dae_RelayBoard",
    version="1.5.2",
    description="Denkovi Relay Board Controller",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Peter Bingham",
    author_email="petersbingham@hotmail.co.uk",
    url="https://code.google.com/p/dae-py-relay-controller/",
    packages=["dae_RelayBoard"],
)
