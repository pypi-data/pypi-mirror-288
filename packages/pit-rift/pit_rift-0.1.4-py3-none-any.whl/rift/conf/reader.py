import configparser
import json
import logging
import os
from collections import OrderedDict
from pathlib import Path

import yaml

logger = logging.getLogger("rift")


def _load_ini_file(f: Path) -> configparser.ConfigParser:
    """
    Load an ini using configparser. Raise an exception if the file doesn't exist

    Args:
        f: Path to the file to load

    Returns: The ini file content

    """
    if not os.path.exists(f):
        raise Exception(f"ERROR ini file '{f}' doesn't exist")

    config = configparser.ConfigParser()
    config.optionxform = str  # to maintain upper case in config_reader file

    # read ini file
    config.read(f)
    return config


def read_ini(f: Path, keep_sections: bool = False) -> dict:
    """

    Args:
        f: Path to the ini file
        keep_sections: Whether to keep sections as keys or flatten the structure

    Returns:
        Dictionary with INI file contents
    """
    config = _load_ini_file(f)

    ini_dict = OrderedDict()
    # Iterate over sections in the INI file
    for section in config.sections():
        if keep_sections:
            ini_dict[section.upper()] = dict(config.items(section))
        else:
            # Flatten the section items into the main dictionary
            for key, value in config.items(section):
                ini_dict[key] = value

    # return to dict to raise an error in case of missing attributes
    return ini_dict


def read_json(f: Path):
    return json.loads(f.read_text())


def read_yaml(f: Path):
    try:
        with open(f) as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {f}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {f} - {e}")
        raise
