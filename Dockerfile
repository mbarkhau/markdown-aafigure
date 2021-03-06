FROM registry.gitlab.com/mbarkhau/markdown_aafigure/base

ADD src/ src/
ADD stubs/ stubs/
ADD test/ test/
ADD requirements/ requirements/
ADD setup.cfg setup.cfg
ADD setup.py setup.py
ADD pylint-ignore.md pylint-ignore.md
ADD README.md README.md
ADD CHANGELOG.md CHANGELOG.md
ADD LICENSE LICENSE
ADD makefile makefile
ADD makefile.bootstrapit.make makefile.bootstrapit.make
ADD scripts/exit_0_if_empty.py scripts/exit_0_if_empty.py

ENV PYTHONPATH="src/:vendor/"

CMD make lint mypy test
