# This file is part of the markdown_aafigure project
# https://gitlab.com/mbarkhau/markdown_aafigure
#
# Copyright (c) 2018-2021 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT


__version__ = "v202103.1010"


from markdown_aafigure.extension import AafigureExtension


def _make_extension(**kwargs) -> AafigureExtension:
    return AafigureExtension(**kwargs)


# Name that conforms with the Markdown extension API
# https://python-markdown.github.io/extensions/api/#dot_notation
makeExtension = _make_extension


__all__ = ['makeExtension', '__version__']
