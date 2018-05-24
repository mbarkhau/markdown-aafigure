#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of markdown-aafigure.
# https://github.com/mbarkhau/markdown-aafigure
# (C) 2018 Manuel Barkhau <mbarkhau@gmail.com>
#
# SPDX-License-Identifier:    MIT

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
    version='0.1.9',
    description='aafigure extension for Python Markdown',
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
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
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
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
