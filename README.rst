Markdown aafigure
==================

.. image:: https://travis-ci.org/mbarkhau/markdown-aafigure.svg?branch=master
    :target: https://travis-ci.org/mbarkhau/markdown-aafigure


This is the `aafigure <https://aafigure.readthedocs.io/>`_
extension for `Python Markdown <https://python-markdown.github.io/>`_

Install
-------

.. code-block::

  $ pip install markdown-aafigure
  $ pip install Pillow    # only for any format other than svg


Use
---

In your markdown text you can define the block:

.. code-block::

  ```aafigure
        +-----+   ^
        |     |   |
    --->+     +---o--->
        |     |   |
        +-----+   V
  ```

Parameters can be set for individual figures.
`Availabale parameters  <http://aafigure.readthedocs.io/en/latest/sphinxext.html#options>`_

.. code-block::

  ```aafigure {"foreground": "#ff0000"}
        +-----+   ^
        |     |   |
    --->+     +---o--->
        |     |   |
        +-----+   V
  ```


Testing
-------


.. code-block::

  $ pip install flake8 pytest pytest-coverage
  $ flake8 src/
  $ python setup.py --quiet install && pytest tests/


MkDocs Integration
------------------

In your mkdocs.yml add this to markdown_extensions.

.. code-block::

  markdown_extensions:
    - markdown_aafigure:
        format: svg
