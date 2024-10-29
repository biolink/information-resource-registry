"""Data test."""
import os
import glob
from linkml_runtime.loaders import yaml_loader
from linkml.generators.pythongen import PythonGenerator
ROOT = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(ROOT, "src", "data", "examples")

EXAMPLE_FILES = glob.glob(os.path.join(DATA_DIR, '*.yaml'))

def test_make_python():
    infile = os.path.join(ROOT, 'src', 'information_resource_registry', 'schema', 'information_resource_registry.yaml')
    pstr = str(PythonGenerator(infile, mergeimports=True).serialize())
    return pstr





