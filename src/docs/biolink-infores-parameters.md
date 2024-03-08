## Biolink Edge Properties for Source Retrieval Provenance

We define the following hierarchy of edge properties in Biolink for capturing Information Resources through which 
knowledge expressed in a given edge was retrieved on its way to its presently serialized form (e.g. a TRAPI message 
sent to an ARA). Full definitions and metadata for each can be found in the Biolink Model.
 
* **biolink:knowledge_source**: 
  * An Information Resource from which the knowledge expressed in an Association was retrieved, 
  directly or indirectly
* **biolink:primary_knowledge_source**: 
  * The most upstream source of the knowledge expressed in an Association that a 
  knowledge provider can identify. 
* **biolink:aggregator_knowledge_source**:  
  * An intermediate aggregator resource from which knowledge expressed in an 
  Association was retrieved downstream of the original source, on its path to its current serialized form.  
* **`biolink:supporting_data_source`**: 
  * An Information Resource from which data was retrieved and subsequently used as
  evidence to generate the knowledge expressed in an Association (e.g. through computation on, reasoning or inference 
  over the retrieved data).


## The Information Resource Registry (infores) data model

An information resource is defined as a web-accessible resource that provides data. An InformationResource 
(designated by its identifier in curie form, e.g. 'infores:monarchintiative') is a Biolink Model class that provides 
a standard way to identify and describe information resources. The InformationResource class details can be found here:
[information_resource_registry.yaml](information_resource_registry.yaml) and contains the following properties:

- **id**: the identifier of the information resource (e.g. 'infores:monarchintiative')
- **name**: the name of the information resource (e.g. 'Monarch Initiative')
- **description**: a description of the information resource (e.g. 'Monarch is a platform for biomedical data discovery 
and integration')
- **url**: the url of the information resource (e.g. 'https://monarchinitiative.org/')
- **status**: the status of the information resource (e.g. 'released', 'deprecated', etc.  Please see the enumeration 
listed in the model yaml for more information)
