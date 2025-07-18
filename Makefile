# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD  ?= sphinx-build
SOURCEDIR    = source
BUILDDIR     = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx-build using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom targets for internationalization
gettext:
	@$(SPHINXBUILD) -b gettext "$(SOURCEDIR)" "$(BUILDDIR)/gettext" $(SPHINXOPTS)
	@echo "Build finished. The message catalogs are in $(BUILDDIR)/gettext."

html-ja:
	@$(SPHINXBUILD) -b html -D language=ja "$(SOURCEDIR)" "$(BUILDDIR)/html-ja" $(SPHINXOPTS)
	@echo "Build finished. The Japanese HTML pages are in $(BUILDDIR)/html-ja."

clean-all:
	rm -rf $(BUILDDIR)/*