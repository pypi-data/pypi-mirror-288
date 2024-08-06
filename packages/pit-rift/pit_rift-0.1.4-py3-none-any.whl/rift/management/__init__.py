import argparse

from rift import core
from rift.management.cli import get_args

def start_from_command_line_interface():
    args: argparse.Namespace = get_args()
    core.execute(**vars(args))
