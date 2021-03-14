<div align="center">
<p align="center">
  <img alt="logo" src="https://gitlab.com/mbarkhau/markdown_aafigure/-/raw/master/logo.png">
</p>
</div>


# [Markdown aafigure][repo_ref]

This is an extension for [Python Markdown](https://python-markdown.github.io/)
which renders diagrams using [aafigure](https://aafigure.readthedocs.io/).

Project/Repo:

[![MIT License][license_img]][license_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]
[![CalVer v202103.1010][version_img]][version_ref]
[![PyPI Version][pypi_img]][pypi_ref]
[![PyPI Downloads][downloads_img]][downloads_ref]

Code Quality/CI:

[![GitHub CI Status][github_build_img]][github_build_ref]
[![GitLab CI Status][gitlab_build_img]][gitlab_build_ref]
[![Type Checked with mypy][mypy_img]][mypy_ref]
[![Code Coverage][codecov_img]][codecov_ref]
[![Code Style: sjfmt][style_img]][style_ref]


|                 Name                |        role       |  since  | until |
|-------------------------------------|-------------------|---------|-------|
| Manuel Barkhau (mbarkhau@gmail.com) | author/maintainer | 2018-05 | -     |


*INFO*: You may want to consider using the [markdown-svgbob](https://pypi.org/project/markdown-svgbob/) extension instead of this one. svgbob has an [online editor](https://ivanceras.github.io/svgbob-editor/) and supports a wider range of shapes and diagrams. Its main disadvantage is that it "only" has builtin support for x86_64 on Windows, Linux and Mac, in contrast to aafigure which is pure python and supported everywhere.


## Install

```bash
$ pip install markdown-aafigure
$ pip install Pillow    # only if you want to render as png
```


## Use

In your markdown text you can define the block:

    ```aafigure
          +-----+   ^
          |     |   |
      --->+     +---o--->
          |     |   |
          +-----+   V
    ```

Parameters can be set for individual figures.
[Availabale parameters](https://aafigure.readthedocs.io/en/latest/sphinxext.html#options)

    ```aafigure {"foreground": "#ff0000"}
          +-----+   ^
          |     |   |
      --->+     +---o--->
          |     |   |
          +-----+   V
    ```


## Development/Testing

```bash
$ git clone https://gitlab.com/mbarkhau/markdown_aafigure
$ cd markdown_aafigure
$ make install
$ make lint mypy test
```


## MkDocs Integration

In your `mkdocs.yml` add this to markdown_extensions.

```yaml
markdown_extensions:
  - markdown_aafigure:
      tag_type: inline_svg
```

Valid options for `tag_type` are `inline_svg` (the default), `img_utf8_svg`, `img_base64_svg`, `img_base64_png`.


[repo_ref]: https://gitlab.com/mbarkhau/markdown_aafigure

[github_build_img]: https://github.com/mbarkhau/markdown-aafigure/workflows/CI/badge.svg
[github_build_ref]: https://github.com/mbarkhau/markdown-aafigure/actions?query=workflow%3ACI

[gitlab_build_img]: https://gitlab.com/mbarkhau/markdown_aafigure/badges/master/pipeline.svg
[gitlab_build_ref]: https://gitlab.com/mbarkhau/markdown_aafigure/pipelines

[codecov_img]: https://gitlab.com/mbarkhau/markdown_aafigure/badges/master/coverage.svg
[codecov_ref]: https://mbarkhau.gitlab.io/markdown_aafigure/cov

[license_img]: https://img.shields.io/badge/License-MIT-blue.svg
[license_ref]: https://gitlab.com/mbarkhau/markdown_aafigure/blob/master/LICENSE

[mypy_img]: https://img.shields.io/badge/mypy-checked-green.svg
[mypy_ref]: https://mbarkhau.gitlab.io/markdown_aafigure/mypycov

[style_img]: https://img.shields.io/badge/code%20style-%20sjfmt-f71.svg
[style_ref]: https://gitlab.com/mbarkhau/straitjacket/

[pypi_img]: https://img.shields.io/badge/PyPI-wheels-green.svg
[pypi_ref]: https://pypi.org/project/markdown_aafigure/#files

[downloads_img]: https://pepy.tech/badge/markdown-aafigure/month
[downloads_ref]: https://pepy.tech/project/markdown-aafigure

[version_img]: https://img.shields.io/static/v1.svg?label=CalVer&message=v202103.1010&color=blue
[version_ref]: https://pypi.org/project/bumpver/

[pyversions_img]: https://img.shields.io/pypi/pyversions/markdown_aafigure.svg
[pyversions_ref]: https://pypi.python.org/pypi/markdown_aafigure

