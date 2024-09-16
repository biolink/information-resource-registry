from __future__ import annotations
from datetime import datetime, date
from enum import Enum

from decimal import Decimal
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel as BaseModel, ConfigDict,  Field, field_validator
import re
import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


metamodel_version = "None"
version = "1.0.0"

class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra = 'forbid',
        arbitrary_types_allowed=True,
        use_enum_values = True)

    pass

        

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
    # Knowledge asserted by a human expert, based on their interpretation of data or published study results
    knowledge_assertion = "knowledge_assertion"
    # Statistical associations calculated between variables in a clinical or omics dataset, by an automated  analysis pipeline
    statistical_association = "statistical_association"
    # Predictions generated computationally through inference over less direct forms of evidence (without human  intervention or review)
    prediction = "prediction"
    # Edge reports a phenomenon that was reported/observed to have occurred (and possibly some quantification,  e.g. how many times, at what frequency)
    observation = "observation"
    # The knowledge level/type fora statement is not provided, typically because it cannot be determined from  available information.
    not_provided = "not_provided"
    # a statement reporting a conclusion that follows logically from premises, which are typically well-established  facts or knowledge assertions. (e.g. fingernail part of finger, finger part of hand → fingernail part of hand)). Logical entailments are based on dedictive inference, and generally have a high degree of confidence when based on sound premises and inference logic.
    logical_entailment = "logical_entailment"
    # A statement that is supported by a mix of different types of evidence, such as a combination of manual  curation and computational prediction. This is a catch-all category for statements that do not fit cleanly  into one of the other categories.
    mixed = "mixed"
    # A knowledge level that does not fit into any of the other categories. This is a catch-all category for  knowledge levels that are not covered by the other categories.
    other = "other"
    
    

class AgentTypeEnum(str, Enum):
    """
    The type of agent that supports an edge or node.  This is a general categorization of the type of agent that supports a statement, and is not intended to be a comprehensive description of the agent.  For example, a statement may be supported by a single publication, but that publication may contain multiple types of evidence, such as a computational prediction and a manual curation.  In this case, the agent type would be "publication", and the evidence would be described in more detail in the evidence graph.
    """
    # a human agent, such as a curator or expert
    manual_agent = "manual_agent"
    # agent type is not provided or known
    not_provided = "not_provided"
    # An automated agent, typically a software program or tool, is responsible for generating the knowledge  expressed in the Edge. Human contribution to the knowledge creation process ends with the definition and  coding of algorithms or analysis pipelines that get executed by the automated agent.
    automated_agent = "automated_agent"
    # An automated agent that executes an analysis workflow over data and reports results in an Edge. These  typically report statistical associations/correlations between variables in the input data.
    data_analysis_pipeline = "data_analysis_pipeline"
    # An automated agent that generates knowledge (typically predictions) based on rules/logic explicitly  encoded in an algorithm (e.g. heuristic models, supervised classifiers), or learned from patterns  observed in data (e.g. ML models, unsupervised classifiers).
    computational_model = "computational_model"
    # An automated agent that uses Natural Language Processing to recognize concepts and/or relationships in text, and generates Edges relating these concepts with formally encoded semantics.
    text_mining_agent = "text_mining_agent"
    # An automated agent that processes images to recognize features and/or relationships in images, and generates  Edges relating these features with formally encoded semantics.
    image_processing_agent = "image_processing_agent"
    # A human agent reviews and validates/approves the veracity of knowledge that is initially generated by an  automated agent.
    manual_validation_of_automated_agent = "manual_validation_of_automated_agent"
    
    

class InformationResourceContainer(ConfiguredBaseModel):
    """
    A collection of information resources
    """
    information_resources: Optional[List[InformationResource]] = Field(default_factory=list, description="""a collection of information resources""")
    
    

class InformationResource(ConfiguredBaseModel):
    """
    A database or knowledgebase and its supporting ecosystem of interfaces  and services that deliver content to consumers (e.g. web portals, APIs,  query endpoints, streaming services, data downloads, etc.). A single Information Resource by this definition may span many different datasets or databases, and include many access endpoints and user interfaces. Information Resources include project-specific resources such as a Translator Knowledge Provider, and community knowledgebases like ChemBL, OMIM, or DGIdb.
    """
    status: Optional[InformationResourceStatusEnum] = Field(None, description="""the status of the infores identifier, the default is \"released\"""")
    name: Optional[str] = Field(None, description="""A human-readable name for an attribute or entity.""")
    id: str = Field(..., description="""A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI""")
    xref: Optional[List[str]] = Field(default_factory=list, description="""A database cross reference or alternative identifier for a NamedThing or edge between two  NamedThings.  This property should point to a database record or webpage that supports the existence of the edge, or  gives more detail about the edge. This property can be used on a node or edge to provide multiple URIs or CURIE cross references.""")
    synonym: Optional[List[str]] = Field(default_factory=list, description="""Alternate human-readable names for a thing""")
    description: Optional[str] = Field(None, description="""A free-text description of an entity or attribute.""")
    knowledge_level: Optional[KnowledgeLevelEnum] = Field(None, description="""The level of knowledge that supports an edge or node.  This is a general categorization of the type of evidence that supports a statement, and is not intended to be a comprehensive description of the evidence.  For example, a statement may be supported by a single publication, but that publication may contain multiple types of evidence, such as a computational prediction and a manual curation.  In this case, the knowledge level would be \"curated\", and the evidence would be described in more detail in the evidence graph.""")
    agent_type: Optional[AgentTypeEnum] = Field(None, description="""The type of agent that supports an edge or node.  This is a general categorization of the type of agent that supports a statement, and is not intended to be a comprehensive description of the agent.  For example, a statement may be supported by a single publication, but that publication may contain multiple types of evidence, such as a computational prediction and a manual curation.  In this case, the agent type would be \"publication\", and the evidence would be described in more detail in the evidence graph.""")
    
    


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
InformationResourceContainer.model_rebuild()
InformationResource.model_rebuild()

