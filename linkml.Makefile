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

infores:
	$(RUN) gen-python src/information_resource_registry/schema/information_resource_registry.yaml > src/information_resource_registry/datamodel/information_resource_registry.py
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
	$(RUN) gen-pydantic --version 2 src/information_resource_registry/schema/information_resource_registry.yaml > $(PYMODEL)/pydanticmodel_v2.py
	$(RUN) gen-owl --mergeimports --no-metaclasses --no-type-objects --add-root-classes --mixins-as-expressions src/information_resource_registry/schema/information_resource_registry.yaml > $(DEST)/owl/information_resource.owl.ttl
	$(MAKE) infores

