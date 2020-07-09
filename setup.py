#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 00:59:44 2020

@author: yue
"""


from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="MFJ",
    version="0.1",
    description="Produced by RDSC for MFJ.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Yue Zhao",
    author_email="yuezhao@rochester.edu",
    install_requires=required,
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
)
