#!/usr/bin/env python

import os
import sys
import httpcache

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Stealing this from Kenneth Reitz
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = ['httpcache']

requires = ['requests>=1.2.0']

setup(
    name='httpcache',
    version=httpcache.__version__,
    description='Simple HTTP cache for Python Requests',
    long_description=open('README.rst').read() + '\n\n' +
                     open('HISTORY.rst').read(),
    author='Cory Benfield',
    author_email='cory@lukasa.co.uk',
    url='http://httpcache.readthedocs.org/en/latest/',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'httpcache': 'httpcache'},
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'),
)
