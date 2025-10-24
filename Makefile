include translator_dataflow.Makefile
include validation.Makefile
include documentation.Makefile
include linkml.Makefile

MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.SUFFIXES:
.SECONDARY:

RUN = poetry run
DOCDIR = docs
RELEASE_TMPDIR = release-output

.PHONY: all clean

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

create_release_extras:
	mkdir -p ${RELEASE_TMPDIR}
	cp infores_catalog.yaml ${RELEASE_TMPDIR}/infores_catalog.yaml
	$(RUN) linkml-convert -s src/information_resource_registry/schema/information_resource_registry.yaml -f yaml -t tsv infores_catalog.yaml > ${RELEASE_TMPDIR}/infores_catalog.tsv
	$(RUN) linkml-convert -s src/information_resource_registry/schema/information_resource_registry.yaml -f yaml -t json infores_catalog.yaml > ${RELEASE_TMPDIR}/infores_catalog.json
	jq -c '.information_resources[]' ${RELEASE_TMPDIR}/infores_catalog.json > ${RELEASE_TMPDIR}/infores_catalog.jsonl


test_pr:
	$(RUN) linkml-validate infores_catalog.yaml -s src/information_resource_registry/schema/information_resource_registry.yaml
	$(RUN) pytest
	$(RUN) codespell
	$(RUN) yamllint -c .yamllint-config src/information_resource_registry/schema/*.yaml
	$(RUN) yamllint -c .yamllint-config infores_catalog.yaml

standardize-data: src/information_resource_registry/standardization/standardize.py infores_catalog.yaml
	$(RUN) python $^ --in-place --schema src/information_resource_registry/schema/information_resource_registry.yaml

sync-rtx-kg2: src/information_resource_registry/translator_dataflow/sync_rtx_kg2_data.py infores_catalog.yaml
	$(RUN) python $<

check_standardized:
	@echo "Checking if infores_catalog.yaml is properly standardized..."
	@cp infores_catalog.yaml /tmp/infores_catalog_backup.yaml
	@$(MAKE) standardize-data
	@if ! diff -q infores_catalog.yaml /tmp/infores_catalog_backup.yaml > /dev/null 2>&1; then \
		cp /tmp/infores_catalog_backup.yaml infores_catalog.yaml; \
		echo ""; \
		echo "ERROR: infores_catalog.yaml is not properly standardized!"; \
		echo "Please run: make standardize-data"; \
		echo ""; \
		rm -f /tmp/infores_catalog_backup.yaml; \
		exit 1; \
	fi
	@rm -f /tmp/infores_catalog_backup.yaml
	@echo "infores_catalog.yaml is properly standardized ✓"

test: check_urls check_standardized
	$(RUN) linkml-validate infores_catalog.yaml -s src/information_resource_registry/schema/information_resource_registry.yaml
	$(RUN) pytest
	$(RUN) codespell
	$(RUN) yamllint -c .yamllint-config src/information_resource_registry/schema/*.yaml
	$(RUN) yamllint -c .yamllint-config infores_catalog.yaml


clean:
	rm -rf $(DEST)
	rm -rf tmp
	rm -fr docs/*
	rm -fr $(PYMODEL)/*

