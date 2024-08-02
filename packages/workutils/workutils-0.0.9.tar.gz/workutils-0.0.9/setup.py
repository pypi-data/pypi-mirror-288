#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree
from setuptools import setup, Command, find_packages

# Package meta-data.
NAME = 'workutils'
DESCRIPTION = 'A tool to solve daily work.'
URL = 'https://github.com/ldspdvsun/workutils'
EMAIL = 'ldspdvsun@gmail.com'
AUTHOR = 'MengYue Sun'
REQUIRES_PYTHON = '>=3.8.0'
VERSION = '0.0.9'

# What packages are required for this module to be executed?
REQUIRED = ['chardet']

# What packages are optional?
EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass
        os.system('{0} setup.py sdist bdist_wheel'.format(sys.executable))
        os.system('twine upload dist/*')
        sys.exit()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=['workutils'],
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    entry_points = {
        'console_scripts': [
            'workutils = workutils.workutils:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
