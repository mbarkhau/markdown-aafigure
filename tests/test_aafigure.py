# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import base64
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


def test_regexp():
    assert ext.AafigureProcessor.RE.match(BASIC_FIG_TXT)


def test_basic_aafigure():
    fig_data = ext.draw_aafigure(BASIC_FIG_TXT, output_fmt='svg')

    assert b"<svg" in fig_data
    assert b"</svg>" in fig_data

    expected = '<p><img src="data:image/svg+xml;utf8,{}" /></p>'.format(
        fig_data.decode('utf-8')
    )

    result = markdown(BASIC_FIG_TXT, extensions=['markdown_aafigure'])

    # with open("debug_img_output_aafigure.svg", mode='wb') as fh:
    #     fh.write(fig_data)
    # with open("debug_img_output_mardown.html", mode='wb') as fh:
    #     fh.write(result.encode('utf-8'))

    result = unescape(result).replace('&quot;', '\"')
    assert result == expected
