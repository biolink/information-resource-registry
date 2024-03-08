## InfoRes Catalog Metadata Dictionary

At present, a minimal set of metadata is being collected in the InfoRes Registry using the following Biolink node 
properties, which will be expanded in future iterations.

name:  a fully informative name for the resource (we recommend a name that is as informative and unambiguous as 
possible - spelling out all acronyms that are not common knowledge, and including the name of the owning organization 
when the name alone may be ambiguous).

id: the CURIE form of the InfoRes identifier, wherein a short form name of the resources serves as a human readable 
identifier component (e.g. ‘infores:dgidb’)

* **synonym**:
  * other names for the resource (will facilitate search/discovery)
* **url**: 
  * a url describing the resource - preferably its primary home page for the resource (if one exists)
* **description**: 
  * a free text description of the resource

## Rules for Minting InfoRes Names and Identifiers

A short form human understandable name or abbreviation is used as the identifier component of an InfoRes IRI, 
and should follow these conventions:

* Use lowercase characters only.
* Keep as short as possible while remaining understandable and unambiguous. 
* Acronyms are good where they are well-established and used in practice in our domain (e.g. infores:omim, not infores:online-mendelian-inheritance-in-man). Otherwise, spell out the name to the extent needed to be understood by the user (e.g. infores:drug-repurposing-hub, not infores:drh).  
* Where it makes sense to do so, adopt the base url of the resources home web address, or its registered prefix in an authority like identifiers.org.
* Use a hyphen (-) to separate words where needed (e.g. infores:drug-repurposing-hub), unless the words are not separated in common practice or the website url (e.g. we use infores:monarchinitiative, not infores:monarch-initiative, because their website is https://monarchinitiative.org/).
* All other non-alphanumeric characters are not allowed as delimiters.
* If we begin creating version-specific identifiers, a dot (.) will be reserved as a separator between the base resource name and its version. And versions will be specified using either dot-separated numerals (e.g. '1.1.2'), or release dates in ISO8601 format (e.g. '2021-04-18').


## Conventions for Crafting Identifiers for Translator Registry Resources

Translator applies many services that wrap or annotate existing resources in APIs to serve content that is better 
aligned with Translator standards. This practice can lead to confusion around what represents a separate Information 
Resource, and how resources may be related to each other. Below we describe conventions we apply for InfoRes creation 
for different scenarios / use cases we encounter in the registry.
 
Aggregator Scenario: KPs/ARAs that aggregate content from one or more existing resource and transform the semantics 
and or structure of the data to be better aligned with Translator standards

Resource Examples:
Molecular Data Provider, Biolink, ROBOKOP, SRI Reference KG, RTX KG2  (these aggregate content from multiple sources into a single KG / API)
Automat APIs (stands up a separate API per source - each of which gets its own InfoRes)