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
<p><img src='data:image/svg+xml;utf8,{}' /></p>
<p>postscript</p>
"""


def test_regexp():
    assert ext.AafigurePreprocessor.RE.match(BASIC_FIG_TXT)


def test_basic_aafigure():
    fig_data = ext.draw_aafigure(BASIC_FIG_TXT, output_fmt='svg')

    assert b"<svg" in fig_data
    assert b"</svg>" in fig_data

    expected = "<p><img src='data:image/svg+xml;utf8,{}' /></p>".format(fig_data.decode('utf-8'))

    result = markdown(BASIC_FIG_TXT, extensions=['markdown_aafigure'])

    # with open("debug_img_output_aafigure.svg", mode='wb') as fh:
    #     fh.write(fig_data)
    # with open("debug_img_output_mardown.html", mode='wb') as fh:
    #     fh.write(result.encode('utf-8'))

    result = unescape(result).replace("&quot;", '\"')
    assert result == expected


def test_param_aafigure():
    fig_data = ext.draw_aafigure(PARAM_FIG_TXT, output_fmt='svg')

    assert b"<svg" in fig_data
    assert b"</svg>" in fig_data
    assert b'stroke="#ff0000"' in fig_data

    result = markdown(PARAM_FIG_TXT, extensions=['markdown_aafigure'])
    result = unescape(result).replace("&quot;", '\"')

    expected = "<p><img src='data:image/svg+xml;utf8,{}' /></p>".format(fig_data.decode('utf-8'))

    expected = expected.replace("\n", "")
    result   = result.replace("\n", "")

    assert result == expected


def test_extended_aafigure():
    fig_data = ext.draw_aafigure(BASIC_FIG_TXT, output_fmt='svg')

    assert b"<svg" in fig_data
    assert b"</svg>" in fig_data

    extensions = DEFAULT_MKDOCS_EXTENSIONS + ['markdown_aafigure']
    result     = markdown(EXTENDED_FIG_TXT, extensions=extensions)
    result     = unescape(result).replace("&quot;", '\"')

    expected = EXTENDED_FIG_HTML_TEMPLATE.format(fig_data.decode('utf-8'))
    expected = expected.replace("\n", "")
    result   = result.replace("\n", "")

    assert result == expected
