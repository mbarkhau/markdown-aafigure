# This file is part of markdown-aafigure.
# https://github.com/mbarkhau/markdown-aafigure
# (C) 2018 Manuel Barkhau <mbarkhau@gmail.com>
#
# SPDX-License-Identifier:    MIT

import re
import json
import base64
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


def fig2img_uri(fig_text: str, output_fmt: str = 'svg') -> str:
    if output_fmt == 'svg':
        mime = "image/svg+xml"
    elif output_fmt == 'png':
        mime = "image/png"
    else:
        raise NotImplementedError(output_fmt)

    img_data    : bytes = draw_aafigure(fig_text, output_fmt=output_fmt)
    img_b64_data: bytes = base64.standard_b64encode(img_data)
    img_b64_text = img_b64_data.decode('ascii')
    return f"data:{mime};base64,{img_b64_text}"


def fig2svg_uri(fig_text: str) -> str:
    return fig2img_uri(fig_text, output_fmt='svg')


def fig2png_uri(fig_text: str) -> str:
    return fig2img_uri(fig_text, output_fmt='png')


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
        is_in_fence = False
        out_lines  : typ.List[str] = []
        block_lines: typ.List[str] = []

        output_fmt: str = self.ext.getConfig('format', 'svg')

        for line in lines:
            if is_in_fence:
                block_lines.append(line)
                if "```" not in line:
                    continue

                is_in_fence = False
                fig_text    = "\n".join(block_lines)
                del block_lines[:]
                img_uri    = fig2img_uri(fig_text, output_fmt=output_fmt)
                img_uri_id = id(img_uri)
                marker     = f"<p id='aafig{img_uri_id}'>aafig{img_uri_id}</p>"
                tag_text   = f"<p><img src='{img_uri}' /></p>"
                out_lines.append(marker)
                self.ext.images[marker] = tag_text
            elif self.RE.match(line):
                is_in_fence = True
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
