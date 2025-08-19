RUN = poetry run

check_urls:
	poetry run check_urls

spell:
	poetry run codespell

lint:
	$(RUN) linkml-lint $(SOURCE_SCHEMA_PATH)

standarize-data: src/information_resource_registry/standardization/standardize.py
	python $< infores_catalog.yaml --in-place -s src/information_resource_registry/schema/information_resource_registry.yaml