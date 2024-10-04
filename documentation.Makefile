RUN = poetry run

# Test documentation locally
serve: mkd-serve

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
	cp $(SRC)/information_resource_registry/schema/information_resource_registry.yaml $(DOCDIR) ; \
	cp $(SRC)/docs/*md $(DOCDIR) ; \
	cp -r $(SRC)/docs/images $(DOCDIR)/images ; \
	# the .json cp here is the data required for the d3 visualizations
	# this supports the display of our d3 visualizations
	cp $(SRC)/docs/*.css $(DOCDIR) ; \
	$(RUN) gen-doc -d $(DOCDIR) --template-directory $(SRC)/$(TEMPLATEDIR) $(SOURCE_SCHEMA_PATH)

testdoc: gendoc serve
