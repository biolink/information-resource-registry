"""information-resource-registry.

A registry of information resources (infores) used in the NCATS Biomedical
Data Translator, together with the LinkML schema that describes it.

The catalog ships inside this package; see
:mod:`information_resource_registry.catalog` for loading it.
"""

from information_resource_registry._version import __version__
from information_resource_registry.catalog import (
    get_catalog_path,
    get_information_resource,
    get_information_resources,
    get_schema_path,
    get_schema_view,
    load_catalog,
    load_catalog_dict,
)

__all__ = [
    "__version__",
    "get_catalog_path",
    "get_information_resource",
    "get_information_resources",
    "get_schema_path",
    "get_schema_view",
    "load_catalog",
    "load_catalog_dict",
]
