#!/usr/bin/env python

import logging
import os
import subprocess
from pathlib import Path

logger = logging.getLogger("rift")


def evaluate_str_with_bash(input_str: str) -> str:
    """
    Retrieves the evaluated value of a Bash-style variable expression.

    Args:
        input_str (str): Input string to be evaluated and resolved.
            e.g., 'foo${var}' or 'foo${var:-"default"}' or $((expr)).
    Returns:
        str: The input str evaluated by the Bash shell.
    Raises:
        ValueError: If an unbound variable is encountered.

    Example:
        >>> evaluate_str_with_bash('foo${var}foo')
        'foobarfoo'
    """
    try:
        result = subprocess.run(
            f"set -o nounset; echo {input_str}",
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        return (
            result.stdout.strip()
        )  # Get the stdout output and strip any extra whitespace
    except subprocess.CalledProcessError as e:
        logger.error(f"Undefined variable: '{input_str}'")
        raise ValueError(f"Undefined variable: '{input_str}'") from e


def export_dict(environ: dict) -> None:
    """
    Export key-value pairs from a dictionary to environment variables.

    Args:
        environ (dict): Dictionary containing variables to export.
    """
    for key, value in environ.items():
        logger.debug(f"Try: export {key}: {value}")

        if value is None:
            logger.warning(f"Skipping variable {key}: {value}")
            continue

        value = str(value).lower() if isinstance(value, bool) else str(value)

        value_to_export = evaluate_str_with_bash(value) if "$" in value else value
        logger.info(f"Export {key} = {value_to_export}")
        os.environ[key] = value_to_export


def add_to_path(p: Path) -> None:
    """
    Args:
        p: Path to append to PATH
    """
    current_env_path = os.environ.get("PATH", "")
    export_dict({"PATH": f"{current_env_path}:{p.as_posix()}"})
