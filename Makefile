MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.SUFFIXES:
.SECONDARY:

RUN = poetry run
# get values from about.yaml file

# basename of a YAML file in model/
.PHONY: all clean

include relation_map.Makefile
include validation.Makefile
include documentation.Makefile
include linkml.Makefile

# note: "help" MUST be the first target in the file,
# when the user types "make" they should get help info
help:
	@echo ""
	@echo "make install -- install dependencies"
	@echo "make test -- runs tests including spelling checks and linting checks"
	@echo "make lint -- perform schema linting"
	@echo "make testdoc -- builds docs and runs local test server"
	@echo "make help -- show this help"
	@echo ""

# install any dependencies required for building
install:
	git init
	poetry install
.PHONY: install

all: site
site: gen-project gendoc

test: test-schema lint spell
	$(RUN) python -m unittest discover -p 'test_*.py'
	$(RUN) codespell
	$(RUN) yamllint -c .yamllint-config src/information_resource_registry.yaml
	$(RUN) yamllint -c .yamllint-config infores_catalog.yaml
	$(RUN) python validation/verify_infores.py

clean:
	rm -rf $(DEST)
	rm -rf tmp
	rm -fr docs/*
	rm -fr $(PYMODEL)/*

