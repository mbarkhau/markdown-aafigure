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


BASIC_BLOCK_TXT = r"""
```aafigure
        +-----+   ^
        |     |   |
    --->+     +---o--->
        |     |   |
        +-----+   V
```
""".strip()


PARAM_BLOCK_TXT = r"""
```aafigure {"foreground": "#ff0000", "line_width": 22}
        +-----+   ^
        |     |   |
    --->+     +---o--->
        |     |   |
        +-----+   V
```
""".strip()


DEFAULT_MKDOCS_EXTENSIONS = ['meta', 'toc', 'tables', 'fenced_code']


EXTENDED_BLOCK_TXT = r"""
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

# Reference image
# https://aafigure.readthedocs.io/en/latest/_images/aafig-2e8a603c57709554ffd252fc56b476eb19b0df6d.svg

ELECTRONICS_EXAMPLE = r"""
                         Q1  _  8MHz
                           || ||
                      +----+| |+----+
                      |    ||_||    |
                      |             |
                +-----+-------------+-----+
                |    XIN           XOUT   |
                |                         |
                |                    P3.3 +--------------+
    SDA/I2C O---+ P2.0                    |              |
                |                         |             e|
                |        MSP430F123       |   +----+  b|/  V1
    SCL/I2C O---+ P2.1               P3.4 +---+ R1 +---+   PNP
                |                         |   +----+   |\
                |           IC1           |      1k     c|    +----+
                |                         |              o----+ R3 +---O TXD/RS232
                |    VCC             GND  |              |    +----+
                +-----+---------------+---+              |      1k
                      |               |                  |    +----+
                      |               |                  +----+ R2 +---O RXD/RS232
                      |               |                       +----+
                      |               |                         10k
    GND/I2C O---o-----+----o----------o-----------o--------------------O GND/RS232
                |     |    |   C1     |           |   C2
               =+=    |  ----- 1u     |         ----- 10u
                      |  ----- 5V +---+---+     ----- 16V
                      |    |      |  GND  |       |            D1|/|
                      +----o------+out  in+-------o----------o---+ +---O RTS/RS232
                                  |  3V   |                  |   |\|
                                  +-------+                  |
                                   IC2                       | D2|/|
                                                             +---+ +---O DTR/RS232
                                                                 |\|
"""


EXTENDED_FIG_HTML_TEMPLATE = r"""
<h1 id="heading">Heading</h1>
<p>prelude</p>
<p>{}</p>
<p>postscript</p>
"""


HTMLTEST_TXT = """
# Heading

prelude

```aafigure {"tag_type":"inline_svg"}
<figtxt>
```

interlude

```aafigure {"tag_type":"img_utf8_svg", "foreground": "#ff0000", "line_width": 4}
<figtxt>
```

interlude

```aafigure {"tag_type":"img_base64_svg"}
<figtxt>
```

interlude

```aafigure {"tag_type":"img_base64_png"}
<figtxt>
```

postscript
"""

HTMLTEST_TXT = HTMLTEST_TXT.replace("<figtxt>", ELECTRONICS_EXAMPLE)


def test_regexp():
    assert ext.AafigurePreprocessor.RE.match(BASIC_BLOCK_TXT)
    assert ext.AafigurePreprocessor.RE.match(BASIC_BLOCK_TXT.replace("```", "~~~"))


def test_determinism_svg_legacy():
    fig_data1 = ext.draw_aafigure(BASIC_BLOCK_TXT, output_fmt='svg')
    fig_data2 = ext.draw_aafigure(BASIC_BLOCK_TXT, output_fmt='svg')
    assert fig_data1 == fig_data2


def test_determinism_svg():
    fig_data1 = ext.draw_aafig(BASIC_BLOCK_TXT, {'tag_type': 'inline_svg'})
    fig_data2 = ext.draw_aafig(BASIC_BLOCK_TXT, {'tag_type': 'inline_svg'})
    assert fig_data1 == fig_data2

    fig_data1 = ext.draw_aafig(BASIC_BLOCK_TXT, {'tag_type': 'img_base64_svg'})
    fig_data2 = ext.draw_aafig(BASIC_BLOCK_TXT, {'tag_type': 'img_base64_svg'})
    assert fig_data1 == fig_data2


def test_basic_svg_aafigure_legacy():
    fig_data = ext.draw_aafigure(BASIC_BLOCK_TXT, output_fmt='svg')

    assert b"<svg" in fig_data
    assert b"</svg>" in fig_data

    img_html = ext.draw_aafig(BASIC_BLOCK_TXT)
    assert img_html.startswith("<svg")
    expected = "<p>{}</p>".format(img_html)

    result = markdown(BASIC_BLOCK_TXT, extensions=['markdown_aafigure'])
    assert img_html in result

    # with open("debug_img_output_aafigure.svg", mode='wb') as fh:
    #     fh.write(fig_data)
    # with open("debug_img_output_mardown.html", mode='wb') as fh:
    #     fh.write(result.encode('utf-8'))

    assert result == expected


def test_basic_png_aafigure_legacy():
    fig_data = ext.draw_aafigure(BASIC_BLOCK_TXT, output_fmt='png')

    img_html = ext.draw_aafig(BASIC_BLOCK_TXT, {'tag_type': 'img_base64_png'})

    img_uri = ext.fig2png_uri(BASIC_BLOCK_TXT)
    assert img_uri.startswith("data:image/png;base64,")
    expected = '<p><img src="{}"/></p>'.format(img_uri)

    result = markdown(
        BASIC_BLOCK_TXT,
        extensions=['markdown_aafigure'],
        extension_configs={'markdown_aafigure': {'format': 'png'}},
    )
    assert img_uri in result

    assert result == expected


def test_param_aafigure():
    fig_html = ext.draw_aafig(PARAM_BLOCK_TXT)

    assert "<svg" in fig_html
    assert "</svg>" in fig_html
    assert 'stroke="#ff0000"' in fig_html

    result = markdown(PARAM_BLOCK_TXT, extensions=['markdown_aafigure'])
    with open("/tmp/aafig_result.html", mode="w") as fh:
        fh.write(result)

    expected = "<p>{}</p>".format(fig_html)

    assert result == expected


def test_extended_aafigure():
    fig_data = ext.draw_aafig(BASIC_BLOCK_TXT)

    assert fig_data.startswith("<svg")
    assert fig_data.endswith("</svg>")

    extensions = DEFAULT_MKDOCS_EXTENSIONS + ['markdown_aafigure']
    result     = markdown(EXTENDED_BLOCK_TXT, extensions=extensions)

    expected = EXTENDED_FIG_HTML_TEMPLATE.format(fig_data)
    expected = expected.replace("\n", "")
    result   = result.replace("\n", "")

    assert result == expected


def test_html_output():
    # NOTE: This generates html that is to be tested
    #   in the browser (for warnings in devtools).
    extensions = DEFAULT_MKDOCS_EXTENSIONS + ['markdown_aafigure']
    result     = markdown(HTMLTEST_TXT, extensions=extensions)
    with open("/tmp/aafigure.html", mode="w") as fh:
        fh.write(result)


if not IS_PIL_INSTALLED:
    test_basic_png_aafigure_legacy = pytest.mark.skip(reason="PIL is not installed")(
        test_basic_png_aafigure_legacy
    )
    test_html_output = pytest.mark.skip(reason="PIL is not installed")(
        test_html_output
    )
