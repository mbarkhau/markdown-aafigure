#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import setuptools


def path(filename):
    dirpath = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(dirpath, filename)


def read(filename):
    with open(path(filename), mode='rb') as fh:
        return fh.read().decode('utf-8')


setuptools.setup(
    name='markdown-aafigure',
    version='0.1.4',
    description='aafigure extension for Python Markdown',
    long_description=read("README.rst"),
    author='Manuel Barkhau',
    author_email='mbarkhau@gmail.com',
    packages=setuptools.find_packages(path("src")),
    package_dir={'': path("src")},
    zip_safe=True,
    url='https://github.com/mbarkhau/markdown-aafigure',
    license='MIT',
    install_requires=[
        'Markdown',
        'aafigure',
    ],
    classifiers=[
        "Development Status :: 3 - Beta",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

)
