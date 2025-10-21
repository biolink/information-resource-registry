# Auto generated from information_resource_registry.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-10-21T15:45:53
# Schema: Information-Resource-Registry-Schema
#
# id: https://w3id.org/biolink/information_resource_registry.yaml
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = "1.0.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
BIOLINK = CurieNamespace('biolink', 'https://w3id.org/biolink/')
INFORES = CurieNamespace('infores', 'https://w3id.org/biolink/infores/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
DEFAULT_ = INFORES


# Types

# Class references



@dataclass(repr=False)
class InformationResourceContainer(YAMLRoot):
    """
    A collection of information resources
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = INFORES["InformationResourceContainer"]
    class_class_curie: ClassVar[str] = "infores:InformationResourceContainer"
    class_name: ClassVar[str] = "InformationResourceContainer"
    class_model_uri: ClassVar[URIRef] = INFORES.InformationResourceContainer

    information_resources: Optional[Union[Union[dict, "InformationResource"], List[Union[dict, "InformationResource"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.information_resources, list):
            self.information_resources = [self.information_resources] if self.information_resources is not None else []
        self.information_resources = [v if isinstance(v, InformationResource) else InformationResource(**as_dict(v)) for v in self.information_resources]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class InformationResource(YAMLRoot):
    """
    A database or knowledgebase and its supporting ecosystem of interfaces and services that deliver content to
    consumers (e.g. web portals, APIs, query endpoints, streaming services, data downloads, etc.). A single
    Information Resource by this definition may span many different datasets or databases, and include many access
    endpoints and user interfaces. Information Resources include project-specific resources such as a Translator
    Knowledge Provider, and community knowledgebases like ChemBL, OMIM, or DGIdb.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = INFORES["InformationResource"]
    class_class_curie: ClassVar[str] = "infores:InformationResource"
    class_name: ClassVar[str] = "InformationResource"
    class_model_uri: ClassVar[URIRef] = INFORES.InformationResource

    status: Union[str, "InformationResourceStatusEnum"] = None
    id: str = None
    name: Optional[str] = None
    xref: Optional[Union[str, List[str]]] = empty_list()
    synonym: Optional[Union[str, List[str]]] = empty_list()
    description: Optional[str] = None
    knowledge_level: Optional[Union[str, "KnowledgeLevelEnum"]] = None
    agent_type: Optional[Union[str, "AgentTypeEnum"]] = None
    consumes: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    consumed_by: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.status):
            self.MissingRequiredField("status")
        if not isinstance(self.status, InformationResourceStatusEnum):
            self.status = InformationResourceStatusEnum(self.status)

        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, str):
            self.id = str(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.xref, list):
            self.xref = [self.xref] if self.xref is not None else []
        self.xref = [v if isinstance(v, str) else str(v) for v in self.xref]

        if not isinstance(self.synonym, list):
            self.synonym = [self.synonym] if self.synonym is not None else []
        self.synonym = [v if isinstance(v, str) else str(v) for v in self.synonym]

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.knowledge_level is not None and not isinstance(self.knowledge_level, KnowledgeLevelEnum):
            self.knowledge_level = KnowledgeLevelEnum(self.knowledge_level)

        if self.agent_type is not None and not isinstance(self.agent_type, AgentTypeEnum):
            self.agent_type = AgentTypeEnum(self.agent_type)

        if not isinstance(self.consumes, list):
            self.consumes = [self.consumes] if self.consumes is not None else []
        self.consumes = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.consumes]

        if not isinstance(self.consumed_by, list):
            self.consumed_by = [self.consumed_by] if self.consumed_by is not None else []
        self.consumed_by = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.consumed_by]

        super().__post_init__(**kwargs)


# Enumerations
class InformationResourceStatusEnum(EnumDefinitionImpl):
    """
    The status of the infores identifier
    """
    released = PermissibleValue(text="released")
    deprecated = PermissibleValue(text="deprecated")
    draft = PermissibleValue(text="draft")
    modified = PermissibleValue(text="modified")

    _defn = EnumDefinition(
        name="InformationResourceStatusEnum",
        description="The status of the infores identifier",
    )

class KnowledgeLevelEnum(EnumDefinitionImpl):
    """
    The level of knowledge that supports an edge or node. This is a general categorization of the type of evidence
    that supports a statement, and is not intended to be a comprehensive description of the evidence. For example, a
    statement may be supported by a single publication, but that publication may contain multiple types of evidence,
    such as a computational prediction and a manual curation. In this case, the knowledge level would be "curated",
    and the evidence would be described in more detail in the evidence graph.
    """
    knowledge_assertion = PermissibleValue(
        text="knowledge_assertion",
        description="""Knowledge asserted by a human expert, based on their interpretation of data or published study results""")
    statistical_association = PermissibleValue(
        text="statistical_association",
        description="""Statistical associations calculated between variables in a clinical or omics dataset, by an automated  analysis pipeline""")
    prediction = PermissibleValue(
        text="prediction",
        description="""Predictions generated computationally through inference over less direct forms of evidence (without human  intervention or review)""")
    observation = PermissibleValue(
        text="observation",
        description="""Edge reports a phenomenon that was reported/observed to have occurred (and possibly some quantification,  e.g. how many times, at what frequency)""")
    not_provided = PermissibleValue(
        text="not_provided",
        description="""The knowledge level/type fora statement is not provided, typically because it cannot be determined from  available information.""")
    logical_entailment = PermissibleValue(
        text="logical_entailment",
        description="""a statement reporting a conclusion that follows logically from premises, which are typically well-established  facts or knowledge assertions. (e.g. fingernail part of finger, finger part of hand → fingernail part of hand)). Logical entailments are based on dedictive inference, and generally have a high degree of confidence when based on sound premises and inference logic.""")
    mixed = PermissibleValue(
        text="mixed",
        description="""A statement that is supported by a mix of different types of evidence, such as a combination of manual  curation and computational prediction. This is a catch-all category for statements that do not fit cleanly  into one of the other categories.""")
    other = PermissibleValue(
        text="other",
        description="""A knowledge level that does not fit into any of the other categories. This is a catch-all category for  knowledge levels that are not covered by the other categories.""")

    _defn = EnumDefinition(
        name="KnowledgeLevelEnum",
        description="""The level of knowledge that supports an edge or node.  This is a general categorization of the type of evidence that supports a statement, and is not intended to be a comprehensive description of the evidence.  For example, a statement may be supported by a single publication, but that publication may contain multiple types of evidence, such as a computational prediction and a manual curation.  In this case, the knowledge level would be \"curated\", and the evidence would be described in more detail in the evidence graph.""",
    )

class AgentTypeEnum(EnumDefinitionImpl):
    """
    The type of agent that supports an edge or node. This is a general categorization of the type of agent that
    supports a statement, and is not intended to be a comprehensive description of the agent. For example, a statement
    may be supported by a single publication, but that publication may contain multiple types of evidence, such as a
    computational prediction and a manual curation. In this case, the agent type would be "publication", and the
    evidence would be described in more detail in the evidence graph.
    """
    manual_agent = PermissibleValue(
        text="manual_agent",
        description="a human agent, such as a curator or expert")
    not_provided = PermissibleValue(
        text="not_provided",
        description="agent type is not provided or known")
    automated_agent = PermissibleValue(
        text="automated_agent",
        description="""An automated agent, typically a software program or tool, is responsible for generating the knowledge  expressed in the Edge. Human contribution to the knowledge creation process ends with the definition and  coding of algorithms or analysis pipelines that get executed by the automated agent.""")
    data_analysis_pipeline = PermissibleValue(
        text="data_analysis_pipeline",
        description="""An automated agent that executes an analysis workflow over data and reports results in an Edge. These  typically report statistical associations/correlations between variables in the input data.""")
    computational_model = PermissibleValue(
        text="computational_model",
        description="""An automated agent that generates knowledge (typically predictions) based on rules/logic explicitly  encoded in an algorithm (e.g. heuristic models, supervised classifiers), or learned from patterns  observed in data (e.g. ML models, unsupervised classifiers).""")
    text_mining_agent = PermissibleValue(
        text="text_mining_agent",
        description="""An automated agent that uses Natural Language Processing to recognize concepts and/or relationships in text, and generates Edges relating these concepts with formally encoded semantics.""")
    image_processing_agent = PermissibleValue(
        text="image_processing_agent",
        description="""An automated agent that processes images to recognize features and/or relationships in images, and generates  Edges relating these features with formally encoded semantics.""")
    manual_validation_of_automated_agent = PermissibleValue(
        text="manual_validation_of_automated_agent",
        description="""A human agent reviews and validates/approves the veracity of knowledge that is initially generated by an  automated agent.""")

    _defn = EnumDefinition(
        name="AgentTypeEnum",
        description="""The type of agent that supports an edge or node.  This is a general categorization of the type of agent that supports a statement, and is not intended to be a comprehensive description of the agent.  For example, a statement may be supported by a single publication, but that publication may contain multiple types of evidence, such as a computational prediction and a manual curation.  In this case, the agent type would be \"publication\", and the evidence would be described in more detail in the evidence graph.""",
    )

# Slots
class slots:
    pass

slots.consumes = Slot(uri=INFORES.consumes, name="consumes", curie=INFORES.curie('consumes'),
                   model_uri=INFORES.consumes, domain=None, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.consumed_by = Slot(uri=INFORES.consumed_by, name="consumed_by", curie=INFORES.curie('consumed_by'),
                   model_uri=INFORES.consumed_by, domain=None, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.status = Slot(uri=INFORES.status, name="status", curie=INFORES.curie('status'),
                   model_uri=INFORES.status, domain=None, range=Union[str, "InformationResourceStatusEnum"])

slots.information_resources = Slot(uri=INFORES.information_resources, name="information_resources", curie=INFORES.curie('information_resources'),
                   model_uri=INFORES.information_resources, domain=None, range=Optional[Union[Union[dict, InformationResource], List[Union[dict, InformationResource]]]])

slots.name = Slot(uri=RDFS.label, name="name", curie=RDFS.curie('label'),
                   model_uri=INFORES.name, domain=None, range=Optional[str])

slots.id = Slot(uri=INFORES.id, name="id", curie=INFORES.curie('id'),
                   model_uri=INFORES.id, domain=None, range=str)

slots.xref = Slot(uri=INFORES.xref, name="xref", curie=INFORES.curie('xref'),
                   model_uri=INFORES.xref, domain=None, range=Optional[Union[str, List[str]]])

slots.synonym = Slot(uri=INFORES.synonym, name="synonym", curie=INFORES.curie('synonym'),
                   model_uri=INFORES.synonym, domain=None, range=Optional[Union[str, List[str]]])

slots.description = Slot(uri=RDFS.comment, name="description", curie=RDFS.curie('comment'),
                   model_uri=INFORES.description, domain=None, range=Optional[str])

slots.knowledge_level = Slot(uri=INFORES.knowledge_level, name="knowledge_level", curie=INFORES.curie('knowledge_level'),
                   model_uri=INFORES.knowledge_level, domain=None, range=Optional[Union[str, "KnowledgeLevelEnum"]])

slots.agent_type = Slot(uri=INFORES.agent_type, name="agent_type", curie=INFORES.curie('agent_type'),
                   model_uri=INFORES.agent_type, domain=None, range=Optional[Union[str, "AgentTypeEnum"]])
