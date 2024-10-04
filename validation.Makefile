RUN = poetry run

validate_infores:
	$(RUN) python src/information_resource_registry/validation/verify_infores.py

spell:
	poetry run codespell

lint:
	$(RUN) linkml-lint $(SOURCE_SCHEMA_PATH)