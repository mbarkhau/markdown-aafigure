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
from xml.sax.saxutils import escape

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor


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


class AafigurePreprocessor(Preprocessor):

    RE = re.compile(r"^```aafigure")

    def __init__(self, md, ext):
        super(AafigurePreprocessor, self).__init__(md)
        self.ext = ext

    def run(self, lines):
        out_lines = []

        fence_marker = None
        block_lines = []

        for line in lines:
            if fence_marker:
                block_lines.append(line)
                if fence_marker in line:
                    fence_marker = None
                    fig_text = "\n".join(block_lines)
                    del block_lines[:]
                    fig_data = draw_aafigure(fig_text, output_fmt='svg')
                    data_uri = 'data:image/svg+xml;utf8,{0}'.format(
                        fig_data.decode('utf-8')
                    )
                    marker = "<p id='aafig{0}'>aafig{0}</p>".format(id(data_uri))
                    out_lines.append(marker)
                    self.ext.images[marker] = "<p><img src='{}' /></p>".format(data_uri)
            else:
                if self.RE.match(line):
                    fence_marker = "```"
                    block_lines.append(line)
                else:
                    out_lines.append(line)

        return out_lines


class AafigurePostprocessor(Postprocessor):

    def __init__(self, md, ext):
        super(AafigurePostprocessor, self).__init__(md)
        self.ext = ext

    def run(self, text):
        print("!!!!!!", repr(text))
        for marker, img in self.ext.images.items():
            wrapped_marker = "<p>" + marker + "</p>"
            if wrapped_marker in text:
                text = text.replace(wrapped_marker, img)
            elif marker in text:
                text = text.replace(marker, img)

        return text


class AafigureExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'format': ['svg', 'Format to use (svg/png)'],
        }
        self.images = {}
        # TODO (mb 2018-05-23): We could have global defaults
        #   instead of an override for each fig. Don't know
        #   how to get the help text automatically though.
        # for k, v in aafigure.aafigure.DEFAULT_OPTIONS.items():
        #     self.config[k] = [v, ??]
        super(AafigureExtension, self).__init__(**kwargs)

    def reset(self):
        self.images.clear()

    def extendMarkdown(self, md, md_globals):
        preproc = AafigurePreprocessor(md, self)
        if 'fenced_code_block' in md.preprocessors:
            md.preprocessors.add('aafigure_fenced_code_block', preproc, '<fenced_code_block')
        else:
            md.preprocessors['aafigure_fenced_code_block'] = preproc

        md.postprocessors['aafigure_fenced_code_block'] = AafigurePostprocessor(md, self)
        md.registerExtension(self)
