# Mapping of file extensions to corresponding reader functions
import os
from pathlib import Path
from typing import Any, Dict, Callable, List

from rift.conf.global_settings import *  # noqa: F403
from rift.conf.mock_settings import *  # noqa: F403
from rift.conf.reader import read_ini, read_json, read_yaml

readers: Dict[Callable, List[str]] = {
    read_json: [".json", ".jsn"],
    read_yaml: [".yaml", ".yml"],
    read_ini: [".ini"],
}


def read_config(f: Path, *args, **kwargs) -> Any:
    """Reads config_reader file using the best strategy and returns dict"""
    # Normalize the file extension
    _, ext = os.path.splitext(f)
    ext = ext.lower()

    # Find the correct reader based on file extension
    for func, exts in readers.items():
        if ext in exts:
            return func(f, *args, **kwargs)

    # If no matching reader is found, raise an error
    raise ValueError(f"Unsupported file extension for file: {f}")
