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

from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


setup(
    name='redminepy',
    version='0.1',
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
    keywords=['redmine', 'api'],
    long_description='__doc__',
    install_requires=['requests'],
    zip_safe=False,
    tests_require=['tox', 'pytest'],
    cmdclass={'test': Tox},
)
