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

import re
import json
import base64

from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree


import aafigure


def draw_aafigure(content, filename=None, output_fmt='svg'):
    if content.startswith("```aafigure"):
        content = content[len("```aafigure"):]
    if content.endswith("```"):
        content = content[:-len("```")]

    options = {'format': output_fmt}
    header, rest = content.split("\n", 1)
    if "{" in header and "}" in header:
        options.update(json.loads(header))
        content = rest

    for option_name in list(options.keys()):
        if option_name not in aafigure.aafigure.DEFAULT_OPTIONS:
            raise ValueError("Invalid Option: {}".format(option_name))

        option_val = options[option_name]
        default_val = aafigure.aafigure.DEFAULT_OPTIONS[option_name]
        default_type = type(default_val)
        if not isinstance(option_val, default_type):
            options[option_name] = default_type(option_val)

    visitor, output = aafigure.render(content, options=options)
    return output.getvalue()


class AafigureProcessor(BlockProcessor):

    RE = re.compile(r"^```aafigure")

    def __init__(self, parser, extension):
        super(AafigureProcessor, self).__init__(parser)
        self.extension = extension

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        fig_blocks = []

        for block in blocks:
            block = block.strip()
            fig_blocks.append(block)
            if block.endswith("```"):
                break

        raw_block = "\n".join(fig_blocks)
        del blocks[:len(fig_blocks)]

        output_fmt = self.extension.getConfig('format')
        fig_data = draw_aafigure(raw_block, output_fmt=output_fmt)
        if output_fmt == 'svg':
            src_data = 'data:image/svg+xml;utf8,{0}'.format(
                fig_data.decode('utf-8')
            )
        elif output_fmt == 'png':
            src_data = 'data:image/png;base64,{0}'.format(
                base64.b64encode(fig_data).decode('ascii')
            )
        else:
            raise Exception("Format not supported: {}".format(output_fmt))

        p = etree.SubElement(parent, 'p')
        img = etree.SubElement(p, 'img')
        img.attrib['src'] = src_data


class AafigureExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'format': ['svg', 'Format to use (svg/png)'],
        }
        # TODO (mb 2018-05-23): We could have global defaults
        #   instead of an override for each fig. Don't know
        #   how to get the help text automatically though.
        # for k, v in aafigure.aafigure.DEFAULT_OPTIONS.items():
        #     self.config[k] = [v, ??]
        super(AafigureExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add(
            'aafigure', AafigureProcessor(md.parser, self), '>indent'
        )
        md.registerExtension(self)
