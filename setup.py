#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ldaphelper
~~~~~~~~~~

Redminepy is a simple Python module for
the Redmine API.

:copyright: (c) 2012 Rafael Römhild
:license: MIT, see LICENSE for more details.
"""

import sys
import redminepy

from setuptools import setup


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='redminepy',
    version=redminepy.__version__,
    author='Rafael Römhild',
    author_email='rafael@roemhild.de',
    description='Python module for the Redmine API.',
    license='MIT',
    packages=['redminepy'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    url='http://github.com/rroemhild/redminepy',
    keywords=['redmine', 'api', 'rest'],
    long_description='__doc__',
    install_requires=required,
    zip_safe=False,
)
