# -*- coding: utf-8 -*-
# This file is part of markdown-aafigure.
# https://github.com/mbarkhau/markdown-aafigure
# (C) 2018 Manuel Barkhau <mbarkhau@gmail.com>
#
# SPDX-License-Identifier:    MIT

import re
import json
import typing as typ

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor


import aafigure


def draw_aafigure(content: str, filename: typ.Any = None, output_fmt: str = 'svg') -> bytes:
    if content.startswith("```aafigure"):
        content = content[len("```aafigure") :]
    if content.endswith("```"):
        content = content[: -len("```")]

    options = {'format': output_fmt}
    header, rest = content.split("\n", 1)
    if "{" in header and "}" in header:
        options.update(json.loads(header))
        content = rest

    for option_name in list(options.keys()):
        if option_name not in aafigure.aafigure.DEFAULT_OPTIONS:
            raise ValueError("Invalid Option: {}".format(option_name))

        option_val   = options[option_name]
        default_val  = aafigure.aafigure.DEFAULT_OPTIONS[option_name]
        default_type = type(default_val)
        if not isinstance(option_val, default_type):
            options[option_name] = default_type(option_val)

    visitor, output = aafigure.render(content, options=options)
    return output.getvalue()


class AafigureExtension(Extension):
    def __init__(self, **kwargs) -> None:
        self.config = {'format': ['svg', "Format to use (svg/png)"]}
        self.images: typ.Dict[str, str] = {}
        # TODO (mb 2018-05-23): We could have global defaults
        #   instead of an override for each fig. Don't know
        #   how to get the help text automatically though.
        # for k, v in aafigure.aafigure.DEFAULT_OPTIONS.items():
        #     self.config[k] = [v, ??]
        super(AafigureExtension, self).__init__(**kwargs)

    def reset(self) -> None:
        self.images.clear()

    def extendMarkdown(self, md, *args, **kwargs) -> None:
        preproc = AafigurePreprocessor(md, self)
        md.preprocessors.register(preproc, name='aafigure_fenced_code_block', priority=50)

        postproc = AafigurePostprocessor(md, self)
        md.postprocessors.register(postproc, name='aafigure_fenced_code_block', priority=0)
        md.registerExtension(self)


class AafigurePreprocessor(Preprocessor):

    RE = re.compile(r"^```aafigure")

    def __init__(self, md, ext: AafigureExtension) -> None:
        super(AafigurePreprocessor, self).__init__(md)
        self.ext: AafigureExtension = ext

    def run(self, lines: typ.List[str]) -> typ.List[str]:
        fence_marker: typ.Optional[str] = None
        out_lines   : typ.List[str] = []
        block_lines : typ.List[str] = []

        for line in lines:
            if fence_marker:
                block_lines.append(line)
                if fence_marker not in line:
                    continue

                fence_marker = None
                fig_text     = "\n".join(block_lines)
                del block_lines[:]
                img_data: bytes = draw_aafigure(fig_text, output_fmt='svg')
                img_text: str   = img_data.decode('utf-8')
                data_uri    = f"data:image/svg+xml;utf8,{img_text}"
                data_uri_id = id(data_uri)
                marker      = f"<p id='aafig{data_uri_id}'>aafig{data_uri_id}</p>"
                img_text    = f"<p><img src='{data_uri}' /></p>"
                out_lines.append(marker)
                self.ext.images[marker] = img_text
            else:
                if self.RE.match(line):
                    fence_marker = "```"
                    block_lines.append(line)
                else:
                    out_lines.append(line)

        return out_lines


class AafigurePostprocessor(Postprocessor):
    def __init__(self, md, ext: AafigureExtension) -> None:
        super(AafigurePostprocessor, self).__init__(md)
        self.ext: AafigureExtension = ext

    def run(self, text: str) -> str:
        for marker, img in self.ext.images.items():
            wrapped_marker = "<p>" + marker + "</p>"
            if wrapped_marker in text:
                text = text.replace(wrapped_marker, img)
            elif marker in text:
                text = text.replace(marker, img)

        return text
