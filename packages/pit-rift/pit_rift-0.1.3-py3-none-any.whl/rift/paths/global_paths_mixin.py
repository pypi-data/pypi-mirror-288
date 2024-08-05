from pathlib import Path

from rift import conf as settings


class GlobalPathsMixin:
    root = Path(__file__).parent.parent.parent
    rift_package = root / "rift"

    shell_package = rift_package / "shell"
    bin_dir = rift_package / "bin"
    conf = rift_package / "conf"

    @classmethod
    def get_load_modules_script(cls):
        return cls.shell_package / settings.LOAD_MODULES

    @classmethod
    def get_starter(cls):
        return cls.shell_package / settings.RIFT_ENTRY_POINT

    @classmethod
    def get_shell_lib_entry_point(cls):
        return cls.shell_package / settings.SHELL_UTILS
