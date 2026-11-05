"""Tests for loading the catalog and schema from the package."""
from pathlib import Path

import yaml

import information_resource_registry
from information_resource_registry import (
    get_catalog_path,
    get_information_resource,
    get_information_resources,
    get_schema_path,
    get_schema_view,
    load_catalog,
    load_catalog_dict,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_version_is_exposed():
    assert isinstance(information_resource_registry.__version__, str)


def test_catalog_path_matches_repo_copy():
    path = get_catalog_path()
    assert path.is_file()
    with open(REPO_ROOT / "infores_catalog.yaml", encoding="utf-8") as fh:
        expected = yaml.safe_load(fh)
    assert load_catalog_dict() == expected


def test_schema_path():
    path = get_schema_path()
    assert path.is_file()
    assert path.name == "information_resource_registry.yaml"


def test_load_catalog_as_pydantic():
    catalog = load_catalog()
    resources = get_information_resources()
    assert len(resources) == len(catalog.information_resources)
    assert len(resources) == len(load_catalog_dict()["information_resources"])
    assert all(r.id.startswith("infores:") for r in resources)


def test_get_information_resource():
    kg2 = get_information_resource("infores:rtx-kg2")
    assert kg2 is not None
    assert kg2.id == "infores:rtx-kg2"
    assert get_information_resource("rtx-kg2") is kg2
    assert get_information_resource("infores:does-not-exist") is None


def test_schema_view():
    sv = get_schema_view()
    assert "InformationResource" in sv.all_classes()
    assert "InformationResourceContainer" in sv.all_classes()
