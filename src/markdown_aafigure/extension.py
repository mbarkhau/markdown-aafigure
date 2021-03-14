# This file is part of the markdown-aafigure project.
# https://gitlab.com/mbarkhau/markdown_aafigure
#
# Copyright (c) 2018-2021 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

import re
import copy
import json
import base64
import typing as typ
import hashlib
import logging
import warnings

import aafigure
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote  # type: ignore


logger = logging.getLogger(__name__)


def make_marker_id(text: str) -> str:
    data = text.encode("utf-8")
    return hashlib.md5(data).hexdigest()


ArgValue = typ.Union[str, int, float, bool]
Options  = typ.Dict[str, ArgValue]

# inline_svg|img_utf8_svg|img_base64_svg|img_base64_png
TagType = str


# <?xml version="1.0" standalone="no"?>
# <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">


def _clean_doctype(img_text: str) -> str:
    img_text = re.sub(r"<\?xml version.*\?>\s*", "", img_text, flags=re.DOTALL)
    img_text = re.sub(r"<!DOCTYPE svg.*?>"     , "", img_text, flags=re.DOTALL)
    return img_text.strip()


def img2html(img_data: bytes, tag_type: TagType = 'inline_svg') -> str:
    if tag_type == 'inline_svg':
        img_text = img_data.decode("utf-8")
        return _clean_doctype(img_text)

    if tag_type == 'img_utf8_svg':
        img_text = img_data.decode("utf-8")
        img_text = quote(img_text)
        return f'<img src="data:image/svg+xml;utf-8,{img_text}"/>'

    if "_base64_" not in tag_type:
        err_msg = f"Invalid tag_type='{tag_type}'"
        raise NotImplementedError(err_msg)

    img_b64_data: bytes = base64.standard_b64encode(img_data)
    img_text = img_b64_data.decode('ascii')

    if tag_type == 'img_base64_png':
        return f'<img src="data:image/png;base64,{img_text}"/>'
    elif tag_type == 'img_base64_svg':
        return f'<img src="data:image/svg+xml;base64,{img_text}"/>'
    else:
        err_msg = f"Invalid tag_type='{tag_type}'"
        raise NotImplementedError(err_msg)


def _clean_block_text(block_text: str) -> str:
    if block_text.startswith("```aafigure"):
        block_text = block_text[len("```aafigure") :]
    elif block_text.startswith("~~~aafigure"):
        block_text = block_text[len("~~~aafigure") :]

    if block_text.endswith("```"):
        block_text = block_text[: -len("```")]
    elif block_text.endswith("~~~"):
        block_text = block_text[: -len("~~~")]
    return block_text


def _parse_block_text(
    block_text: str, default_options: Options = None
) -> typ.Tuple[str, TagType, Options]:
    block_text = _clean_block_text(block_text)
    header, rest = block_text.split("\n", 1)

    options: Options = {}

    if default_options:
        options.update(default_options)

    if "{" in header and "}" in header:
        options.update(json.loads(header))
        block_text = rest

    tag_type = typ.cast(TagType, options.pop('tag_type', 'inline_svg'))

    if tag_type.endswith("_svg"):
        output_fmt = 'svg'
    elif tag_type.endswith("_png"):
        output_fmt = 'png'
    else:
        err_msg = f"Invalid tag_type='{tag_type}'"
        raise NotImplementedError(err_msg)

    options['format'] = output_fmt

    for option_name in list(options.keys()):
        if option_name not in aafigure.aafigure.DEFAULT_OPTIONS:
            raise ValueError("Invalid Option: {}".format(option_name))

        option_val   = options[option_name]
        default_val  = aafigure.aafigure.DEFAULT_OPTIONS[option_name]
        default_type = type(default_val)
        if not isinstance(option_val, default_type):
            options[option_name] = default_type(option_val)

    return (block_text, tag_type, options)


def draw_aafig(block_text: str, default_options: Options = None) -> str:
    block_text, tag_type, options = _parse_block_text(block_text, default_options)

    _, output = aafigure.render(block_text, options=options)
    img_data = output.getvalue()
    return img2html(img_data, tag_type)


# Depricated API which probably nobody is using directly.


def draw_aafigure(block_text: str, filename: typ.Any = None, output_fmt: str = 'svg') -> bytes:
    # pylint:disable=unused-argument
    warnings.warn("draw_aafigure is depricated use 'draw_aafig' instead", DeprecationWarning)
    if output_fmt == 'png':
        tag_type = 'img_base64_png'
    elif output_fmt == 'svg':
        tag_type = 'img_base64_svg'
    elif output_fmt == 'svg':
        tag_type = 'img_utf8_svg'
    else:
        tag_type = 'img_base64_svg'

    default_options: Options = {'tag_type': tag_type}
    block_text, tag_type, options = _parse_block_text(block_text, default_options)

    _, output = aafigure.render(block_text, options=options)
    result = output.getvalue()
    if isinstance(result, str):
        return result.encode("utf-8")
    if isinstance(result, bytes):
        return result

    errmsg = f"Unexpected return type from aafigure.render: {type(result)}"
    raise TypeError(errmsg)


def fig2img_uri(block_text: str, output_fmt: str = 'svg', encoding: str = 'base64') -> str:
    warnings.warn("fig2img_uri is depricated use 'draw_aafig' instead", DeprecationWarning)
    if output_fmt == 'png':
        tag_type = 'img_base64_png'
    elif output_fmt == 'svg' and encoding == 'utf-8':
        tag_type = 'img_utf8_svg'
    elif output_fmt == 'svg' and encoding == 'base64':
        tag_type = 'img_base64_svg'
    else:
        tag_type = 'img_base64_svg'

    default_options: Options = {'tag_type': tag_type}
    tag_html = draw_aafig(block_text, default_options)
    return tag_html[len('<img src="') : -len('"/>')]


def fig2svg_uri(block_text: str) -> str:
    return fig2img_uri(block_text, output_fmt='svg')


def fig2png_uri(block_text: str) -> str:
    return fig2img_uri(block_text, output_fmt='png')


DEFAULT_CONFIG = {
    # prior to v201904.0005 the config paramter
    #   was format, but the prefered parameter
    #   going forward is tag_type.
    'format'  : ['svg', "Legacy parameter for output format"],
    'tag_type': [
        'inline_svg',
        "Format to use (inline_svg|img_utf8_svg|img_base64_svg|img_base64_png)",
    ],
    # NOTE: This is taken from the output of
    #   aafigure --help which unfortunately is
    #   not easilly programatically available.
    'widechars'     : ["", "unicode properties to be treated as wide glyph (e.g. 'F,W,A')"],
    'debug'         : ["", "enable debug outputs"],
    'textual'       : ["", "disable horizontal fill detection"],
    'textual_strict': ["", "disable horizontal and vertical fill detection"],
    'scale'         : ["", "set scale"],
    'aspect'        : ["", "set aspect ratio"],
    'line_width'    : ["", "set width, svg only"],
    'proportional'  : ["", "use proportional font instead of fixed width"],
    'foreground'    : ["", "foreground color default=#000000"],
    'fill'          : ["", "foreground color default=foreground"],
    'background'    : ["", "background color default=#ffffff"],
    'rounded'       : ["", "use arcs for rounded edges instead of straight lines"],
}


class AafigureExtension(Extension):
    def __init__(self, **kwargs) -> None:
        self.config = copy.deepcopy(DEFAULT_CONFIG)
        self.images: typ.Dict[str, str] = {}
        super().__init__(**kwargs)

    def reset(self) -> None:
        self.images.clear()

    def extendMarkdown(self, md) -> None:
        preproc = AafigurePreprocessor(md, self)
        md.preprocessors.register(preproc, name='aafigure_fenced_code_block', priority=50)

        postproc = AafigurePostprocessor(md, self)
        md.postprocessors.register(postproc, name='aafigure_fenced_code_block', priority=0)
        md.registerExtension(self)


BLOCK_RE = re.compile(r"^(```|~~~)aafigure")


class AafigurePreprocessor(Preprocessor):
    def __init__(self, md, ext: AafigureExtension) -> None:
        super().__init__(md)
        self.ext: AafigureExtension = ext

    @property
    def default_options(self) -> Options:
        options: Options = {}

        for name in self.ext.config.keys():
            val = self.ext.getConfig(name, "")
            if val != "":
                options[name] = val

        output_fmt   : typ.Any = options.get('format')
        if output_fmt:
            if output_fmt == 'png':
                override_tag_type = 'img_base64_png'
            elif output_fmt == 'svg':
                override_tag_type = 'inline_svg'
            else:
                override_tag_type = 'inline_svg'
            options['tag_type'] = override_tag_type

        return options

    def _make_tag_for_block(self, block_lines: typ.List[str]) -> str:
        block_text = "\n".join(block_lines).rstrip()
        img_tag    = draw_aafig(block_text, self.default_options)
        img_id     = make_marker_id(img_tag)
        marker_tag = f"<p id=\"tmp_md_aafig{img_id}\">aafig{img_id}</p>"
        tag_text   = f"<p>{img_tag}</p>"
        self.ext.images[marker_tag] = tag_text
        return marker_tag

    def _iter_out_lines(self, lines: typ.List[str]) -> typ.Iterable[str]:
        is_in_fence          = False
        expected_close_fence = "```"

        block_lines: typ.List[str] = []

        for line in lines:
            if is_in_fence:
                block_lines.append(line)
                is_ending_fence = line.strip() == expected_close_fence
                if not is_ending_fence:
                    continue

                is_in_fence = False
                marker_tag  = self._make_tag_for_block(block_lines)
                del block_lines[:]
                yield marker_tag
            else:
                fence_match = BLOCK_RE.match(line)
                if fence_match:
                    is_in_fence          = True
                    expected_close_fence = fence_match.group(1)
                    block_lines.append(line)
                else:
                    yield line

    def run(self, lines: typ.List[str]) -> typ.List[str]:
        return list(self._iter_out_lines(lines))


# NOTE (mb):
#   Q: Why this business with the Postprocessor? Why
#   not just do `yield tag_text` and save the hassle
#   of `self.ext.math_html[marker_tag] = tag_text` ?
#   A: Maybe there are other processors that can't be
#   trusted to leave the inserted markup alone. Maybe
#   the inserted markup could be incorrectly parsed as
#   valid markdown.


class AafigurePostprocessor(Postprocessor):
    def __init__(self, md, ext: AafigureExtension) -> None:
        super().__init__(md)
        self.ext: AafigureExtension = ext

    def run(self, text: str) -> str:
        for marker_tag, img in self.ext.images.items():
            if marker_tag in text:
                wrapped_marker = "<p>" + marker_tag + "</p>"
                while marker_tag in text:
                    if wrapped_marker in text:
                        text = text.replace(wrapped_marker, img)
                    else:
                        text = text.replace(marker_tag, img)
            else:
                logger.warning(f"AafigurePostprocessor couldn't find: {marker_tag}")

        return text
