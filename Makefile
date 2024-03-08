MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.SUFFIXES:
.SECONDARY:

RUN = poetry run
# get values from about.yaml file
SCHEMA_NAME = $(shell ${SHELL} ./utils/get-value.sh name)
SOURCE_SCHEMA_PATH = $(shell ${SHELL} ./utils/get-value.sh source_schema_path)
SOURCE_SCHEMA_DIR = $(dir $(SOURCE_SCHEMA_PATH))
SRC = src
DEST = project
PYMODEL = $(SRC)/information_resource_registry/datamodel
DOCDIR = docs
EXAMPLEDIR = examples
TEMPLATEDIR = doc-templates

# environment variables
include config.env

GEN_PARGS =
ifdef LINKML_GENERATORS_PROJECT_ARGS
GEN_PARGS = ${LINKML_GENERATORS_PROJECT_ARGS}
endif

GEN_DARGS =
ifdef LINKML_GENERATORS_MARKDOWN_ARGS
GEN_DARGS = ${LINKML_GENERATORS_MARKDOWN_ARGS}
endif


# basename of a YAML file in model/
.PHONY: all clean

# note: "help" MUST be the first target in the file,
# when the user types "make" they should get help info
help: status
	@echo ""
	@echo "make site -- makes site locally"
	@echo "make install -- install dependencies"
	@echo "make test -- runs tests"
	@echo "make lint -- perform linting"
	@echo "make testdoc -- builds docs and runs local test server"
	@echo "make deploy -- deploys site"
	@echo "make update -- updates linkml version"
	@echo "make help -- show this help"
	@echo ""

status: check-config
	@echo "Project: $(SCHEMA_NAME)"
	@echo "Source: $(SOURCE_SCHEMA_PATH)"

# generate products and add everything to github
setup: install gen-project gen-examples gendoc git-init-add

# install any dependencies required for building
install:
	git init
	poetry install
.PHONY: install

# ---
# Project Synchronization
# ---
#
# check we are up to date
check: cruft-check
cruft-check:
	cruft check
cruft-diff:
	cruft diff

update: update-template update-linkml
update-template:
	cruft update

# todo: consider pinning to template
update-linkml:
	poetry add -D linkml@latest

all: site
site: gen-project gendoc
%.yaml: gen-project
deploy: all mkd-gh-deploy

# In future this will be done by conversion
gen-examples:
	cp src/data/examples/* $(EXAMPLEDIR)

infores:
	$(RUN) gen-python src/information_resource_registry/schema/information_resource_registry.yaml > src/information_resource_registry/datamodel/information_resource_registry.py

validate_infores:
	$(RUN) python src/information_resource_registry/scripts/verify_infores.py

spell:
	poetry run codespell

# generates all project files

gen-project: $(PYMODEL)
	# keep these in sync between PROJECT_FOLDERS and the includes/excludes for gen-project and test-schema
	$(RUN) gen-project \
		--exclude excel \
		--include graphql \
		--include jsonld \
		--exclude markdown \
		--include prefixmap \
		--include proto \
		--include shacl \
		--include shex \
		--exclude sqlddl \
		--include jsonldcontext \
		--include jsonschema \
		--exclude owl \
		--include python \
		--include rdf \
		-d $(DEST) $(SOURCE_SCHEMA_PATH)
	$(RUN) gen-pydantic --pydantic-version 1 src/information_resource_registry/schema/information_resource_registry.yaml > $(PYMODEL)/pydanticmodel.py
	$(RUN) gen-pydantic --pydantic-version 2 src/information_resource_registry/schema/information_resource_registry.yaml > $(PYMODEL)/pydanticmodel_v2.py
	$(RUN) gen-owl --mergeimports --no-metaclasses --no-type-objects --add-root-classes --mixins-as-expressions src/information_resource_registry/schema/information_resource_registry.yaml > $(DEST)/owl/information_resource.owl.ttl
	$(MAKE) infores

tests:
	$(RUN) python -m unittest discover -p 'test_*.py'
	$(RUN) codespell
	$(RUN) yamllint -c .yamllint-config src/information_resource_registry.yaml
	$(RUN) yamllint -c .yamllint-config infores_catalog.yaml
	$(RUN) python scripts/verify_infores.py

test: test-schema test-python test-examples lint spell tests validate_infores

test-schema: gen-project

test-python:
	$(RUN) python -m unittest discover -p 'test_*.py'

lint:
	$(RUN) linkml-lint $(SOURCE_SCHEMA_PATH)

convert-examples-to-%:
	$(patsubst %, $(RUN) linkml-convert  % -s $(SOURCE_SCHEMA_PATH) -C Person, $(shell ${SHELL} find src/data/examples -name "*.yaml"))

examples/%.yaml: src/data/examples/%.yaml
	$(RUN) linkml-convert -s $(SOURCE_SCHEMA_PATH) -C Person $< -o $@
examples/%.json: src/data/examples/%.yaml
	$(RUN) linkml-convert -s $(SOURCE_SCHEMA_PATH) -C Person $< -o $@
examples/%.ttl: src/data/examples/%.yaml
	$(RUN) linkml-convert -P EXAMPLE=http://example.org/ -s $(SOURCE_SCHEMA_PATH) -C Person $< -o $@

test-examples: examples/output

examples/output: src/information_resource_registry/schema/information_resource_registry.yaml
	mkdir -p $@
	$(RUN) linkml-run-examples \
		--output-formats json \
		--output-formats yaml \
		--counter-example-input-directory src/data/examples/invalid \
		--input-directory src/data/examples/valid \
		--output-directory $@ \
		--schema $< > $@/README.md

# Test documentation locally
serve: mkd-serve

# Python datamodel
$(PYMODEL):
	mkdir -p $@


$(DOCDIR):
	mkdir -p $@

gen-viz:
	$(RUN) generate_viz_json

gendoc: $(DOCDIR)
	# DO NOT REMOVE: these cp statements are crucial to maintain the w3 ids for the model artifacts
	cp $(DEST)/owl/information_resource_registry.owl.ttl $(DOCDIR)/information_resource_registry.owl.ttl ; \
	cp $(DEST)/jsonld/information_resource_registry.context.jsonld $(DOCDIR)/information_resource_registry.context.jsonld ; \
	cp $(DEST)/jsonld/information_resource_registry.context.jsonld $(DOCDIR)/context.jsonld ; \
	cp $(DEST)/jsonld/information_resource_registry.jsonld $(DOCDIR)/information_resource_registry.jsonld ; \
	cp $(DEST)/jsonschema/information_resource_registry.schema.json $(DOCDIR)/information_resource_registry.json ; \
	cp $(DEST)/graphql/information_resource_registry.graphql $(DOCDIR)/information_resource_registry.graphql ; \
	cp $(DEST)/shex/information_resource_registry.shex $(DOCDIR)/information_resource_registryn.shex ; \
	cp $(DEST)/shacl/information_resource_registry.shacl.ttl $(DOCDIR)/information_resource_registry.shacl.ttl ; \
	cp infores_catalog.yaml $(DOCDIR) ; \
	cp $(SRC)/schema/information_resource_registry/information_resource_registry.yaml $(DOCDIR) ; \
	cp $(SRC)/docs/*md $(DOCDIR) ; \
	cp -r $(SRC)/docs/images $(DOCDIR)/images ; \
	# the .json cp here is the data required for the d3 visualizations
	# this supports the display of our d3 visualizations
	cp $(SRC)/docs/*.css $(DOCDIR) ; \
	$(RUN) gen-doc -d $(DOCDIR) --template-directory $(SRC)/$(TEMPLATEDIR) $(SOURCE_SCHEMA_PATH)


testdoc: gendoc serve

MKDOCS = $(RUN) mkdocs
mkd-%:
	$(MKDOCS) $*

PROJECT_FOLDERS = sqlschema shex shacl protobuf prefixmap owl jsonschema jsonld graphql excel
git-init-add: git-init git-add git-commit git-status
git-init:
	git init
git-add: .cruft.json
	git add .gitignore .github .cruft.json Makefile LICENSE *.md examples utils about.yaml mkdocs.yml poetry.lock project.Makefile pyproject.toml src/information_resource_registry/schema/*yaml src/*/datamodel/*py src/data src/docs tests src/*/_version.py
	git add $(patsubst %, project/%, $(PROJECT_FOLDERS))
git-commit:
	git commit -m 'chore: initial commit' -a
git-status:
	git status

# only necessary if setting up via cookiecutter
.cruft.json:
	echo "creating a stub for .cruft.json. IMPORTANT: setup via cruft not cookiecutter recommended!" ; \
	touch $@

clean:
	rm -rf $(DEST)
	rm -rf tmp
	rm -fr docs/*
	rm -fr $(PYMODEL)/*

include project.Makefile
