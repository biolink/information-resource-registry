from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "1.0.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_curi_maps': ['obo_context',
                           'idot_context',
                           'monarch_context',
                           'semweb_context'],
     'default_prefix': 'infores',
     'default_range': 'string',
     'id': 'https://w3id.org/biolink/information_resource_registry.yaml',
     'imports': ['linkml:types'],
     'license': 'https://creativecommons.org/publicdomain/zero/1.0/',
     'name': 'Information-Resource-Registry-Schema',
     'prefixes': {'biolink': {'prefix_prefix': 'biolink',
                              'prefix_reference': 'https://w3id.org/biolink/'},
                  'infores': {'prefix_prefix': 'infores',
                              'prefix_reference': 'https://w3id.org/biolink/infores/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'}},
     'source_file': 'src/information_resource_registry/schema/information_resource_registry.yaml'} )

class InformationResourceStatusEnum(str, Enum):
    """
    The status of the infores identifier
    """
    released = "released"
    deprecated = "deprecated"
    draft = "draft"
    modified = "modified"


class KnowledgeLevelEnum(str, Enum):
    """
    The level of knowledge that supports an edge or node.  This is a general categorization of the type of evidence that supports a statement, and is not intended to be a comprehensive description of the evidence.  For example, a statement may be supported by a single publication, but that publication may contain multiple types of evidence, such as a computational prediction and a manual curation.  In this case, the knowledge level would be "curated", and the evidence would be described in more detail in the evidence graph.
    """
    knowledge_assertion = "knowledge_assertion"
    """
    Knowledge asserted by a human expert, based on their interpretation of data or published study results
    """
    statistical_association = "statistical_association"
    """
    Statistical associations calculated between variables in a clinical or omics dataset, by an automated  analysis pipeline
    """
    prediction = "prediction"
    """
    Predictions generated computationally through inference over less direct forms of evidence (without human  intervention or review)
    """
    observation = "observation"
    """
    Edge reports a phenomenon that was reported/observed to have occurred (and possibly some quantification,  e.g. how many times, at what frequency)
    """
    not_provided = "not_provided"
    """
    The knowledge level/type fora statement is not provided, typically because it cannot be determined from  available information.
    """
    logical_entailment = "logical_entailment"
    """
    a statement reporting a conclusion that follows logically from premises, which are typically well-established  facts or knowledge assertions. (e.g. fingernail part of finger, finger part of hand → fingernail part of hand)). Logical entailments are based on dedictive inference, and generally have a high degree of confidence when based on sound premises and inference logic.
    """
    mixed = "mixed"
    """
    A statement that is supported by a mix of different types of evidence, such as a combination of manual  curation and computational prediction. This is a catch-all category for statements that do not fit cleanly  into one of the other categories.
    """
    other = "other"
    """
    A knowledge level that does not fit into any of the other categories. This is a catch-all category for  knowledge levels that are not covered by the other categories.
    """


class AgentTypeEnum(str, Enum):
    """
    The type of agent that supports an edge or node.  This is a general categorization of the type of agent that supports a statement, and is not intended to be a comprehensive description of the agent.  For example, a statement may be supported by a single publication, but that publication may contain multiple types of evidence, such as a computational prediction and a manual curation.  In this case, the agent type would be "publication", and the evidence would be described in more detail in the evidence graph.
    """
    manual_agent = "manual_agent"
    """
    a human agent, such as a curator or expert
    """
    not_provided = "not_provided"
    """
    agent type is not provided or known
    """
    automated_agent = "automated_agent"
    """
    An automated agent, typically a software program or tool, is responsible for generating the knowledge  expressed in the Edge. Human contribution to the knowledge creation process ends with the definition and  coding of algorithms or analysis pipelines that get executed by the automated agent.
    """
    data_analysis_pipeline = "data_analysis_pipeline"
    """
    An automated agent that executes an analysis workflow over data and reports results in an Edge. These  typically report statistical associations/correlations between variables in the input data.
    """
    computational_model = "computational_model"
    """
    An automated agent that generates knowledge (typically predictions) based on rules/logic explicitly  encoded in an algorithm (e.g. heuristic models, supervised classifiers), or learned from patterns  observed in data (e.g. ML models, unsupervised classifiers).
    """
    text_mining_agent = "text_mining_agent"
    """
    An automated agent that uses Natural Language Processing to recognize concepts and/or relationships in text, and generates Edges relating these concepts with formally encoded semantics.
    """
    image_processing_agent = "image_processing_agent"
    """
    An automated agent that processes images to recognize features and/or relationships in images, and generates  Edges relating these features with formally encoded semantics.
    """
    manual_validation_of_automated_agent = "manual_validation_of_automated_agent"
    """
    A human agent reviews and validates/approves the veracity of knowledge that is initially generated by an  automated agent.
    """



class InformationResourceContainer(ConfiguredBaseModel):
    """
    A collection of information resources
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/biolink/information_resource_registry.yaml',
         'tree_root': True})

    information_resources: Optional[list[InformationResource]] = Field(default=None, description="""a collection of information resources""", json_schema_extra = { "linkml_meta": {'alias': 'information_resources',
         'domain_of': ['InformationResourceContainer']} })


class InformationResource(ConfiguredBaseModel):
    """
    A database or knowledgebase and its supporting ecosystem of interfaces  and services that deliver content to consumers (e.g. web portals, APIs,  query endpoints, streaming services, data downloads, etc.). A single Information Resource by this definition may span many different datasets or databases, and include many access endpoints and user interfaces. Information Resources include project-specific resources such as a Translator Knowledge Provider, and community knowledgebases like ChemBL, OMIM, or DGIdb.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['knowledgebase'],
         'from_schema': 'https://w3id.org/biolink/information_resource_registry.yaml',
         'rules': [{'postconditions': {'slot_conditions': {'agent_type': {'name': 'agent_type',
                                                                          'required': True},
                                                           'knowledge_level': {'name': 'knowledge_level',
                                                                               'required': True}}},
                    'preconditions': {'slot_conditions': {'status': {'equals_string': 'released',
                                                                     'name': 'status'}}}}]})

    status: InformationResourceStatusEnum = Field(default=..., description="""the status of the infores identifier, the default is \"released\"""", json_schema_extra = { "linkml_meta": {'alias': 'status', 'domain_of': ['InformationResource']} })
    name: str = Field(default=..., description="""A human-readable name for an attribute or entity.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'aliases': ['label', 'display name', 'title'],
         'domain_of': ['InformationResource'],
         'slot_uri': 'rdfs:label'} })
    id: str = Field(default=..., description="""A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['InformationResource']} })
    xref: Optional[list[str]] = Field(default=None, description="""A database cross reference or alternative identifier for a NamedThing or edge between two  NamedThings.  This property should point to a database record or webpage that supports the existence of the edge, or  gives more detail about the edge. This property can be used on a node or edge to provide multiple URIs or CURIE cross references.""", json_schema_extra = { "linkml_meta": {'alias': 'xref',
         'aliases': ['dbxref', 'Dbxref', 'DbXref', 'record_url', 'source_record_urls'],
         'domain_of': ['InformationResource']} })
    synonym: Optional[list[str]] = Field(default=None, description="""Alternate human-readable names for a thing""", json_schema_extra = { "linkml_meta": {'alias': 'synonym', 'aliases': ['alias'], 'domain_of': ['InformationResource']} })
    description: Optional[str] = Field(default=None, description="""A free-text description of an entity or attribute.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'aliases': ['comment', 'note', 'definition', 'description'],
         'domain_of': ['InformationResource'],
         'slot_uri': 'rdfs:comment'} })
    knowledge_level: Optional[KnowledgeLevelEnum] = Field(default=None, description="""The level of knowledge that supports an edge or node.  This is a general categorization of the type of evidence that supports a statement, and is not intended to be a comprehensive description of the evidence.  For example, a statement may be supported by a single publication, but that publication may contain multiple types of evidence, such as a computational prediction and a manual curation.  In this case, the knowledge level would be \"curated\", and the evidence would be described in more detail in the evidence graph.""", json_schema_extra = { "linkml_meta": {'alias': 'knowledge_level', 'domain_of': ['InformationResource']} })
    agent_type: Optional[AgentTypeEnum] = Field(default=None, description="""The type of agent that supports an edge or node.  This is a general categorization of the type of agent that supports a statement, and is not intended to be a comprehensive description of the agent.  For example, a statement may be supported by a single publication, but that publication may contain multiple types of evidence, such as a computational prediction and a manual curation.  In this case, the agent type would be \"publication\", and the evidence would be described in more detail in the evidence graph.""", json_schema_extra = { "linkml_meta": {'alias': 'agent_type', 'domain_of': ['InformationResource']} })
    consumes: Optional[list[str]] = Field(default=None, description="""A collection of information resources that are consumed by this information resource""", json_schema_extra = { "linkml_meta": {'alias': 'consumes', 'domain_of': ['InformationResource']} })
    consumed_by: Optional[list[str]] = Field(default=None, description="""A collection of information resources that consume this information resource""", json_schema_extra = { "linkml_meta": {'alias': 'consumed_by', 'domain_of': ['InformationResource']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
InformationResourceContainer.model_rebuild()
InformationResource.model_rebuild()

