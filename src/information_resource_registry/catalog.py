"""Access to the infores catalog and schema bundled with this package.

Typical use::

    from information_resource_registry import get_information_resource, load_catalog

    catalog = load_catalog()                # pydantic InformationResourceContainer
    kg2 = get_information_resource("infores:rtx-kg2")
    print(kg2.name, kg2.knowledge_level)

The canonical copy of the catalog is ``infores_catalog.yaml`` at the root of the
GitHub repository. When the package is built it is copied to
``information_resource_registry/data/infores_catalog.yaml``; when running from
a source checkout (for example an editable install) the root copy is used.
"""

from __future__ import annotations

from functools import lru_cache
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

import yaml

if TYPE_CHECKING:
    from linkml_runtime import SchemaView

    from information_resource_registry.datamodel.pydanticmodel_v2 import (
        InformationResource,
        InformationResourceContainer,
    )

PACKAGE_NAME = "information_resource_registry"
CATALOG_FILENAME = "infores_catalog.yaml"
SCHEMA_FILENAME = "information_resource_registry.yaml"

__all__ = [
    "CATALOG_FILENAME",
    "SCHEMA_FILENAME",
    "get_catalog_path",
    "get_information_resource",
    "get_information_resources",
    "get_schema_path",
    "get_schema_view",
    "load_catalog",
    "load_catalog_dict",
]


def get_catalog_path() -> Path:
    """Return the path of the infores catalog YAML file.

    Prefers the copy bundled in the installed package, falling back to the
    repository-root copy when running from a source checkout.
    """
    packaged = files(PACKAGE_NAME).joinpath("data", CATALOG_FILENAME)
    if packaged.is_file():
        return Path(str(packaged))
    repo_root_copy = Path(__file__).resolve().parents[2] / CATALOG_FILENAME
    if repo_root_copy.is_file():
        return repo_root_copy
    raise FileNotFoundError(
        f"{CATALOG_FILENAME} was not found in the installed package or the source tree"
    )


def get_schema_path() -> Path:
    """Return the path of the LinkML schema that describes the catalog."""
    return Path(str(files(PACKAGE_NAME).joinpath("schema", SCHEMA_FILENAME)))


def load_catalog_dict() -> dict[str, Any]:
    """Load the catalog as plain Python data (the parsed YAML document)."""
    with get_catalog_path().open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@lru_cache(maxsize=1)
def load_catalog() -> "InformationResourceContainer":
    """Load the catalog as a validated pydantic ``InformationResourceContainer``.

    The result is cached; it is a shared object, so treat it as read-only.
    """
    from information_resource_registry.datamodel.pydanticmodel_v2 import (
        InformationResourceContainer,
    )

    return InformationResourceContainer.model_validate(load_catalog_dict())


def get_information_resources() -> list["InformationResource"]:
    """Return every information resource in the catalog, including deprecated ones."""
    return list(load_catalog().information_resources or [])


@lru_cache(maxsize=1)
def _resources_by_id() -> dict[str, "InformationResource"]:
    return {resource.id: resource for resource in get_information_resources()}


def get_information_resource(infores_id: str) -> Optional["InformationResource"]:
    """Look up a resource by its CURIE, e.g. ``"infores:rtx-kg2"``.

    A bare identifier without the ``infores:`` prefix is also accepted.
    Returns ``None`` if the identifier is not in the catalog.
    """
    if ":" not in infores_id:
        infores_id = f"infores:{infores_id}"
    return _resources_by_id().get(infores_id)


def get_schema_view() -> "SchemaView":
    """Return a linkml-runtime ``SchemaView`` over the packaged schema."""
    from linkml_runtime import SchemaView

    return SchemaView(str(get_schema_path()))
