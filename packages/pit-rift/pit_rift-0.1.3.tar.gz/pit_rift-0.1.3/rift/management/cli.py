import argparse
import importlib.metadata
import sys
from pathlib import Path

from rift import core


def get_args(raw_args=None) -> argparse.Namespace:
    parse = argparse.ArgumentParser(description="MedSea Test Automation Framework")
    # General args
    parse.add_argument("test_case_config", type=Path, help="Path of test case")
    parse.add_argument(
        "-v",
        dest="verbose",
        default=4,
        type=int,
        help="Verbose level from 1 (CRITICAL) to 5 (DEBUG). Default is 4 (INFO)",
    )
    parse.add_argument(
        "-w",
        dest="work_dir",
        type=Path,
        default=None,
        help="To change the test working dir. Default is ini_test_case_YYYYMMDDTHHmmss",
    )
    parse.add_argument(
        "-i",
        "--init",
        dest="to_initialize",
        default=False,
        action="store_true",
        help="If the test case doesn't exist, create it",
    )
    parse.add_argument(
        "-V",
        "--version",
        dest="get_version",
        default=False,
        action="store_true",
        help="Print version and exit",
    )

    if "-V" in sys.argv or "--version" in sys.argv:
        print(importlib.metadata.version("pit-rift"))
        sys.exit(0)
    return parse.parse_args(raw_args)


if __name__ == "__main__":
    args: argparse.Namespace = get_args()
    core.execute(**vars(args))
