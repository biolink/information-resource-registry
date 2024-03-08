from __future__ import annotations
from datetime import datetime, date
from enum import Enum

from decimal import Decimal
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel as BaseModel, Field, validator
import re
import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


metamodel_version = "None"
version = "1.0.0"

class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'

class ConfiguredBaseModel(WeakRefShimBaseModel,
                validate_assignment = True,
                validate_all = True,
                underscore_attrs_are_private = True,
                extra = 'forbid',
                arbitrary_types_allowed = True,
                use_enum_values = True):

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
    # knowledge generated through manual curation  or interpretation of data or published study results
    curated = "curated"
    # predictions generated computationally through inference over less direct forms of evidence (without human  intervention or review)
    predicted = "predicted"
    # knowledge extracted from published text by NLP agents (without human intervention or review)
    text_mined = "text_mined"
    # statistical correlations calculated between variables in a clinical or omics dataset, by an automated  analysis pipeline
    correlation = "correlation"
    # edge reports a phenomenon that was reported/observed to have occurred (and possibly some quantification,  e.g. how many times, at what frequency)
    observed = "observed"
    # knowledge level may not fit into the categories above, or is not provided/known
    other = "other"
    # used for sources that might provide edges with different knowledge levels, e.g.correlations in addition to  curated Edges - set tag to Curated, unless predicate rules override
    mixed = "mixed"
    
    

class AgentTypeEnum(str, Enum):
    """
    The type of agent that supports an edge or node.  This is a general categorization of the type of agent that supports a statement, and is not intended to be a comprehensive description of the agent.  For example, a statement may be supported by a single publication, but that publication may contain multiple types of evidence, such as a computational prediction and a manual curation.  In this case, the agent type would be "publication", and the evidence would be described in more detail in the evidence graph.
    """
    # agent type is not provided or known
    not_provided = "not_provided"
    # a computational model, such as a machine learning model
    computational_model = "computational_model"
    
    

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
    
    


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
InformationResourceContainer.update_forward_refs()
InformationResource.update_forward_refs()

