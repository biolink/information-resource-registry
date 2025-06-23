RUN = poetry run

check_urls:
	poetry run check_urls

spell:
	poetry run codespell

lint:
	$(RUN) linkml-lint $(SOURCE_SCHEMA_PATH)