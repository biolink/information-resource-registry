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





