We have created a InfoRes Catalog here, to store these identifiers along with metadata about the Information Resource 
they specify. Data creators should consult the ‘id’ column of the InfoRes Catalog to find CURIEs for specific 
Information Resources. Use these CURIEs to populate the ‘value’ field in an Attribute object that uses one of the 
source retrieval provenance edge properties described above as its key. 
   
## Adding a new Information Resource entry: 

If there is no record in the catalog for a given resource, users should make a pull request that adds a row for the 
missing resource. Minimally, add the ‘name’ and ‘url’ for the resource.  The 'url' field should point to a page in 
the Translator Resource Wiki: https://github.com/NCATSTranslator/Translator-All/wiki/.  Please at least have a stub wiki
page filled out for any new information resource added to the catalog via a pull request.  Information about the format
of the wiki page can be found in the [Translator Resource Wiki](https://github.com/NCATSTranslator/Translator-All/wiki/).

Please also suggest an infores CURIE in the ‘id’ field, (see [Appendices 1 and 2](appendices.md) for more guidance).  
PRs will require a review.  

## Editing metadata for an existing entry: 

KP / ARA representatives can create a pull request to add or edit the metadata provided for an existing resource in 
much the same manner as adding a new resource.  Please note, that a record that is no longer being used or should 
otherwise be "deprecated" should set the "status" field in an information resource record to "deprecated" instead
of being deleted from the registry.  This helps maintain provenance of the ids minted in this registry.

## Modifying an existing Information Resource entry in the registry:

Making changes to the registry to the information-resource-registry GitHub repository.  Any of the 
fields in an Information Resource entry can be modified, but the id field must not be changed.  If the id field is
changed, it must be treated as a new entry and the old entry must be deprecated. This gives downstream applications
a chance to update their records to reflect the change and keeps links to the existing resource from breaking.

## Adding a new Information Resource entry to the registry: 

Adding a new entry to the registry is as easy as adding a stanza to the infores_catalog.yaml file in the
repository and submitting the change via pull request.  Alternatively, making a ticket for a new
resource in the information-resource-registry GitHub repository will also work.  

## Minting new Information Resource identifiers:

- Each smartAPI-registered Translator API gets its own InfoRes, as will each upstream source from which it aggregates knowledge.
  - Each upstream source from which a Translator API retrieves data computed on to generate knowledge will also get its own InfoRes.
- Identifiers should be short, readable, strings delimited with a dash ('-').  These identifiers will be used 
in user-facing applications and should be as readable as possible.
- In general, the 'status' field of an Information Resource stanza should be one of two values: 'released' or 'deprecated'.

The following is an example of a new entry in the
infores_catalog.yaml file:
```
- id: infores:my-new-resource
  name: My New Resource
  description: This is a new resource
  url: https://github.com/NCATSTranslator/Translator-All/wiki/my-new-resource
  status: released
```

## Removing an infores stanza from the registry:

In an effort to maintain the integrity of the applications that use the Information Resource Registry identifiers downstream, 
we will not be removing entries from the registry.  But, if an information resource is no longer available, we will
mark it as deprecated in the registry and downstream applications will no longer
serve deprecated Information Resources from their methods.  