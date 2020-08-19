#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 18:21:46 2020

@author: wanghaojie
"""

from setuptools import setup

setup(
   name='CrunchbaseAPI',
   version='1.0',
   description='An API of Crunchbase',
   author='Haojie Wang',
   author_email='775371789@qq.com',
   packages=['CrunchbaseAPI'],  #same as name
   install_requires=['json', 'requests','pandas','datetime','concurrent'], #external packages as dependencies
)
