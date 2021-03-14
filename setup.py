# This file is part of the markdown_aafigure project
# https://gitlab.com/mbarkhau/markdown_aafigure
#
# Copyright (c) 2019-2020 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

import os
import sys
import setuptools


def project_path(*sub_paths):
    project_dirpath = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(project_dirpath, *sub_paths)


def read(*sub_paths):
    with open(project_path(*sub_paths), mode="rb") as fh:
        return fh.read().decode("utf-8")


package_dir = {"": "src"}

if any(arg.startswith("bdist") for arg in sys.argv):
    import lib3to6
    package_dir = lib3to6.fix(package_dir)


install_requires = [
    line.strip()
    for line in read("requirements", "pypi.txt").splitlines()
    if line.strip() and not line.startswith("#")
]


long_description = "\n\n".join((read("README.md"), read("CHANGELOG.md")))


setuptools.setup(
    name="markdown_aafigure",
    license="MIT",
    author="Manuel Barkhau",
    author_email="mbarkhau@gmail.com",
    url="https://gitlab.com/mbarkhau/markdown_aafigure",
    version="202103.1010",
    keywords="markdown aafigure extension",
    description="aafigure extension for Python Markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["markdown_aafigure"],
    package_dir=package_dir,
    install_requires=install_requires,
    zip_safe=True,
    entry_points={
        'markdown.extensions': [
            'markdown_aafigure = markdown_aafigure.extension:AafigureExtension',
        ]
    },

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
