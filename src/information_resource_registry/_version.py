from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("information-resource-registry")
except PackageNotFoundError:
    # package not installed
    __version__ = "0.0.0"
