# Changelog for https://gitlab.com/mbarkhau/markdown_aafigure

## v202103.1010

 - Fix related to [#14](https://gitlab.com/mbarkhau/markdown-katex/-/issues/14): Since `Markdown>=3.3` support for [Markdown in HTML][md_in_html] was broken.

[md_in_html]: https://python-markdown.github.io/extensions/md_in_html/


## v202001.0009

 - Fix: Ignore trailing whitespace after closing fence.


## v202001.0008

 - Fix: Bad image substitution when markdown has multiple diagrams


## v201907.0006

 - Fix: don't require typing package for py<35


## v201904.0005

 - Add: Support for inline svg
 - Add: `tag_type` option for better control of embedding
 - Depricated: `format` parameter


## v201904.0004

 - Add: Support of format: png extension configuration (requires Pillow)
 - Fix: Use base64 encoding for image uri


## v201904.0003

 - Fix #3: escape xml in image data uri
 - Fix: cleanup debug output
 - Change: Move to gitlab.com/mbarkhau/markdown-aafigure
 - Change: Switch to pycalver
 - Change: Project packaging updates


## 0.2.0 (2018-05-28)

 - Initial release
