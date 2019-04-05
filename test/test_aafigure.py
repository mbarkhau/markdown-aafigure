# -*- coding: utf-8 -*-
# This file is part of markdown-aafigure.
# https://github.com/mbarkhau/markdown-aafigure
# (C) 2018 Manuel Barkhau <mbarkhau@gmail.com>
#
# SPDX-License-Identifier:    MIT

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from xml.sax.saxutils import unescape

from markdown import markdown
import markdown_aafigure.extension as ext

import pytest

try:
    import PIL

    IS_PIL_INSTALLED = True
except ImportError:
    IS_PIL_INSTALLED = False


BASIC_FIG_TXT = r"""
```aafigure
        +-----+   ^
        |     |   |
    --->+     +---o--->
        |     |   |
        +-----+   V
```
""".strip()


PARAM_FIG_TXT = r"""
```aafigure {"foreground": "#ff0000", "line_width": 22}
        +-----+   ^
        |     |   |
    --->+     +---o--->
        |     |   |
        +-----+   V
```
""".strip()


DEFAULT_MKDOCS_EXTENSIONS = ['meta', 'toc', 'tables', 'fenced_code']


EXTENDED_FIG_TXT = r"""
# Heading

prelude

```aafigure
        +-----+   ^
        |     |   |
    --->+     +---o--->
        |     |   |
        +-----+   V
```

postscript
"""


EXTENDED_FIG_HTML_TEMPLATE = r"""
<h1 id="heading">Heading</h1>
<p>prelude</p>
<p><img src='{}' /></p>
<p>postscript</p>
"""


def test_regexp():
    assert ext.AafigurePreprocessor.RE.match(BASIC_FIG_TXT)


def test_basic_svg_aafigure():
    fig_data = ext.draw_aafigure(BASIC_FIG_TXT, output_fmt='svg')

    assert b"<svg" in fig_data
    assert b"</svg>" in fig_data

    img_uri = ext.fig2svg_uri(BASIC_FIG_TXT)
    assert img_uri.startswith("data:image/svg+xml;base64,")
    expected = "<p><img src='{}' /></p>".format(img_uri)

    result = markdown(BASIC_FIG_TXT, extensions=['markdown_aafigure'])
    assert img_uri in result

    # with open("debug_img_output_aafigure.svg", mode='wb') as fh:
    #     fh.write(fig_data)
    # with open("debug_img_output_mardown.html", mode='wb') as fh:
    #     fh.write(result.encode('utf-8'))

    assert result == expected


def test_basic_png_aafigure():
    fig_data = ext.draw_aafigure(BASIC_FIG_TXT, output_fmt='png')

    img_uri = ext.fig2png_uri(BASIC_FIG_TXT)
    assert img_uri.startswith("data:image/png;base64,")
    expected = "<p><img src='{}' /></p>".format(img_uri)

    result = markdown(
        BASIC_FIG_TXT,
        extensions=['markdown_aafigure'],
        extension_configs={'markdown_aafigure': {'format': 'png'}},
    )
    assert img_uri in result

    assert result == expected


if not IS_PIL_INSTALLED:
    test_basic_png_aafigure = pytest.mark.skip(reason="PIL is not installed")(
        test_basic_png_aafigure
    )


def test_param_aafigure():
    fig_data = ext.draw_aafigure(PARAM_FIG_TXT, output_fmt='svg')

    assert b"<svg" in fig_data
    assert b"</svg>" in fig_data
    assert b'stroke="#ff0000"' in fig_data

    result = markdown(PARAM_FIG_TXT, extensions=['markdown_aafigure'])

    img_uri  = ext.fig2svg_uri(PARAM_FIG_TXT)
    expected = "<p><img src='{}' /></p>".format(img_uri)

    assert result == expected


def test_extended_aafigure():
    fig_data = ext.draw_aafigure(BASIC_FIG_TXT, output_fmt='svg')

    assert b"<svg" in fig_data
    assert b"</svg>" in fig_data

    extensions = DEFAULT_MKDOCS_EXTENSIONS + ['markdown_aafigure']
    result     = markdown(EXTENDED_FIG_TXT, extensions=extensions)

    img_uri  = ext.fig2svg_uri(BASIC_FIG_TXT)
    expected = EXTENDED_FIG_HTML_TEMPLATE.format(img_uri)
    expected = expected.replace("\n", "")
    result   = result.replace("\n", "")

    assert result == expected
