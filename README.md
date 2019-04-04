# [Markdown aafigure][repo_ref]

This is an extension for [Python Markdown](https://python-markdown.github.io/)
which can render diagrams using [aafigure](https://aafigure.readthedocs.io/).

Project/Repo:

[![MIT License][license_img]][license_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]
[![PyCalVer v201904.0002][version_img]][version_ref]
[![PyPI Version][pypi_img]][pypi_ref]
[![PyPI Downloads][downloads_img]][downloads_ref]

Code Quality/CI:

[![Build Status][build_img]][build_ref]
[![Type Checked with mypy][mypy_img]][mypy_ref]
[![Code Coverage][codecov_img]][codecov_ref]
[![Code Style: sjfmt][style_img]][style_ref]


|                 Name                |        role       |  since  | until |
|-------------------------------------|-------------------|---------|-------|
| Manuel Barkhau (mbarkhau@gmail.com) | author/maintainer | 2018-05 | -     |


## Install

```bash
$ pip install markdown-aafigure
$ pip install Pillow    # only for any format other than svg
```

## Use

In your markdown text you can define the block:

```
\`\`\`aafigure
      +-----+   ^
      |     |   |
  --->+     +---o--->
      |     |   |
      +-----+   V
\`\`\`
```

Parameters can be set for individual figures.
[Availabale parameters](https://aafigure.readthedocs.io/en/latest/sphinxext.html#options)

```
\`\`\`aafigure {"foreground": "#ff0000"}
      +-----+   ^
      |     |   |
  --->+     +---o--->
      |     |   |
      +-----+   V
\`\`\`
```

## Testing

```bash
$ cd markdown-aafigure
$ make install
$ make lint mypy test
```

## MkDocs Integration

In your `mkdocs.yml` add this to markdown_extensions.

```yaml
markdown_extensions:
  - markdown_aafigure:
      format: svg
```

[repo_ref]: https://gitlab.com/mbarkhau/markdown_aafigure

[build_img]: https://gitlab.com/mbarkhau/markdown_aafigure/badges/master/pipeline.svg
[build_ref]: https://gitlab.com/mbarkhau/markdown_aafigure/pipelines

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

[version_img]: https://img.shields.io/static/v1.svg?label=PyCalVer&message=v201904.0002&color=blue
[version_ref]: https://pypi.org/project/pycalver/

[pyversions_img]: https://img.shields.io/pypi/pyversions/markdown_aafigure.svg
[pyversions_ref]: https://pypi.python.org/pypi/markdown_aafigure

