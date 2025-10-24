RUN = uv run

check_urls:
	$(RUN) check_urls

spell:
	$(RUN) codespell

lint:
	$(RUN) linkml-lint $(SOURCE_SCHEMA_PATH)
