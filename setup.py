#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:任向民
# datetime:2019/1/2 14:11
# software: PyCharm

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)