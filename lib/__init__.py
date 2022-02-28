import os
import yaml

BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'data')

with open(os.path.join(BASE_PATH, 'parameters.yml'), 'r') as yaml_file:
    PARAMETERS = yaml.safe_load(yaml_file)

API_URLS = PARAMETERS["URLS"]
