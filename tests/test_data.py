"""Data test."""
import os
import glob
from pathlib import Path
from information_resource_registry.validation.check_urls import is_valid_url
import yaml
from linkml.generators.pythongen import PythonGenerator
ROOT = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(ROOT, "src", "data", "examples")

EXAMPLE_FILES = glob.glob(os.path.join(DATA_DIR, '*.yaml'))
schemal_yaml =  file_path = Path(__file__).parent.parent / 'src' / 'information_resource_registry' / 'schema' / 'information_resource_registry.yaml'
infores_catalog =  file_path = Path(__file__).parent.parent / 'infores_catalog.yaml'

def test_make_python() -> str:
    """
    Generate python code from a schema

    :return: python code as string
    """
    pstr = str(PythonGenerator(schemal_yaml, mergeimports=True).serialize())
    return pstr


def test_catalog_schema_validation():
    with open(infores_catalog, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
        assert data.get('information_resources') is not None
        for infores in data.get("information_resources"):
            if infores.get('status') != "deprecated":
                assert infores.get('knowledge_level') is not None
                assert infores.get('agent_type') is not None


def test_multiomics_renamed_infores_entries():
    with open(infores_catalog, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)

    resources = data.get("information_resources", [])
    by_id = {infores.get("id"): infores for infores in resources}
    resource_ids = set(by_id.keys())

    renamed_pairs = {
        "infores:clinicaltrials": "infores:clinicaltrials-gov",
        "infores:multiomics-clinicaltrials": "infores:clinicaltrials-kp",
        "infores:multiomics-drugapprovals": "infores:drugapprovals-kp",
        "infores:multiomics-microbiome": "infores:microbiome-kp",
        "infores:multiomics-multiomics": "infores:multiomics-kp",
    }

    for old_id, new_id in renamed_pairs.items():
        assert new_id in resource_ids
        assert old_id in resource_ids
        assert by_id[old_id].get("status") == "deprecated"

    cqs_consumes = set(by_id["infores:cqs"].get("consumes", []))
    rtx_kg2_consumes = set(by_id["infores:rtx-kg2"].get("consumes", []))

    assert "infores:clinicaltrials-kp" in cqs_consumes
    assert "infores:multiomics-ctkp" not in cqs_consumes
    assert "infores:clinicaltrials-kp" in rtx_kg2_consumes
    assert "infores:biothings-multiomics-clinicaltrials" not in rtx_kg2_consumes

    old_ids = set(renamed_pairs.keys())
    for infores in resources:
        assert not old_ids.intersection(infores.get("consumes", []))
        assert not old_ids.intersection(infores.get("consumed_by", []))


