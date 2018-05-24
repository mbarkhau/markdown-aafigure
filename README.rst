Markdown aafigure
==================

.. image:: https://travis-ci.org/mbarkhau/markdown-aafigure.svg?branch=master
    :target: https://travis-ci.org/mbarkhau/markdown-aafigure


This is the `aafigure <https://aafigure.readthedocs.io/>`_
extension for `Python Markdown <https://python-markdown.github.io/>`_

Install
-------

.. code-block:: bash

    $ pip install markdown-aafigure
    $ pip install Pillow    # only for any format other than svg


Use
---

In your markdown text you can define the block:

.. code-block:: text

    ```aafigure
          +-----+   ^
          |     |   |
      --->+     +---o--->
          |     |   |
          +-----+   V
    ```

Parameters can be set for individual figures.
`Availabale parameters  <https://aafigure.readthedocs.io/en/latest/sphinxext.html#options>`_

.. code-block:: text

    ```aafigure {"foreground": "#ff0000"}
          +-----+   ^
          |     |   |
      --->+     +---o--->
          |     |   |
          +-----+   V
    ```


Testing
-------


.. code-block:: bash

    $ pip install flake8 pytest pytest-coverage rs2html5
    $ flake8 src/
    $ python setup.py --long-description | rst2html5 --strict > README.html
    $ python setup.py --quiet install --force; pytest -v --cov=markdown_aafigure --cov-report term-missing tests/


Publish
-------

.. code-block:: bash

    $ rm dist/*; python setup.py sdist bdist_wheel upload


MkDocs Integration
------------------

In your mkdocs.yml add this to markdown_extensions.

.. code-block:: yaml

    markdown_extensions:
      - markdown_aafigure:
          format: svg
