import os
from sstc_core.sites.spectral.io_tools import load_yaml

config_dirpath = os.path.dirname(os.path.abspath(__file__))


yaml_filename = "catalog_default_filepaths.yaml"
catalog_filepaths = load_yaml(os.path.join(config_dirpath, yaml_filename))


