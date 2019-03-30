#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'praktipy'
DESCRIPTION = 'A small toolbox for physics laboratory courses at the TU Dortmund.'
URL = 'https://github.com/The-Ludwig/praktipy'
AUTHOR = 'Ludwig Neste <The-Ludwig>, Max Uetrecht <phenomax>'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None

REQUIRED = [
    'matplotlib', 'uncertainties', 'numpy', 'pint', 'scipy'
]

DEV_REQUIRED = [
    'twine'
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    extras_require={
        'dev': DEV_REQUIRED,
    },
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Natural Language :: German',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Education'
    ],
)
