# This file is part of the markdown_aafigure project
# https://gitlab.com/mbarkhau/markdown_aafigure
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from markdown_aafigure.extension import AafigureExtension


def makeExtension(**kwargs):
    return AafigureExtension(**kwargs)
