import os
import sys
from yaml import safe_load


def load_config():
    # If the code from line 7 to line 10 doesn't open the "config.yml"
    # file correctly to read the configurations, please uncomment lines 11 to 13 and run the application again.
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    target_path = os.path.join(curr_dir, "..", "..", "config.yml")
    with open(target_path, "r") as yml:
        return safe_load(yml)
    # root_dir = os.path.dirname(sys.modules["__main__"].__file__)
    # with open(root_dir + "\\config.yml", "r") as yml:
    #     return safe_load(yml)


def get_entry():
    config = load_config()
    return config["database"]["storage_path"]
