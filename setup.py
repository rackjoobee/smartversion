#!/usr/bin/env python

# Setup code borrowed from Kenneth Reitz's excellent Requests:
# http://python-requests.org

import smartversion

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()

vers = smartversion.__version__

setup(
    name = 'smartversion',
    version = vers,
    description = 'Easy software version parsing/manipulation',
    long_description = readme + '\n\n' + history,
    author='Jack Ruby',
    author_email='j0hnruby@vfemail.net',
    url='https://github.com/j0hnruby/smartversion',
    download_url='https://github.com/j0hnruby/smartversion/tarball/' + vers,
    packages=['smartversion'],
    install_requires=[],
    license='MIT',
    keywords=['version', 'parsing', 'looseversion'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',    
        #'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',        
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: Software Development :: Version Control',
        'Topic :: Internet',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
    ],
)
