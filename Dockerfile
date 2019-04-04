FROM registry.gitlab.com/mbarkhau/markdown_aafigure/base

ADD src/ src/
ADD stubs/ stubs/
ADD test/ test/
ADD requirements/ requirements/
ADD setup.cfg setup.cfg
ADD setup.py setup.py
ADD README.md README.md
ADD CHANGELOG.md CHANGELOG.md
ADD LICENSE LICENSE
ADD makefile makefile
ADD makefile.config.make makefile.config.make
ADD makefile.extra.make makefile.extra.make

CMD make serve