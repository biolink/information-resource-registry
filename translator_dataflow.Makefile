MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.SUFFIXES:
.SECONDARY:

### Sankey generation

## Generate all the JSON files that define "consumes" relationships

DATA_DIR = "src/information_resource_registry/translator_dataflow/data"
RUN = uv run

sankey: generate_consumes_annotations merge_into_infores_catalog generate_sankey

generate_consumes_annotations:
	$(RUN) rtx_kg2
	$(RUN) bte_sp
	$(RUN) arax_kps
	$(RUN) aragorn_kps
	$(RUN) unsecret
	$(RUN) molepro_consume

merge_into_infores_catalog:
	$(RUN) add_consume_info infores_catalog.yaml ${DATA_DIR}/*.json > ${DATA_DIR}/infores_catalog_new.yaml
	mv $(DATA_DIR)/infores_catalog_new.yaml infores_catalog.yaml


generate_sankey:
	$(RUN) extract_consume_info infores_catalog.yaml $(DATA_DIR)/consume_info.csv
	$(RUN) generate_sankey $(DATA_DIR)/consume_info.csv
