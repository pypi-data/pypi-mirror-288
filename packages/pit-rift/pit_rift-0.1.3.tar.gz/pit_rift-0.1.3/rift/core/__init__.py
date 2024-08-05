
import rift
from rift.core import main
from rift.core import scheduler


def execute(**kwargs):
    rift.setup()
    kwargs.pop("verbose")
    get_version = kwargs.pop("get_version")

    if get_version:
        exit(0)

    main.execute(**kwargs)
