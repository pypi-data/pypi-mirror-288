from datetime import datetime
from pathlib import Path
from typing import Dict

from rift.model import TestCase
from rift.paths.execution_paths_mixin import ExecutionPathsMixin
from rift.paths.global_paths_mixin import GlobalPathsMixin
from rift.paths.test_case_paths_mixin import TestCasePathsMixin


def timestamp():
    return datetime.now().strftime("%Y%m%dT%H%M%S")


class PathManager(GlobalPathsMixin, ExecutionPathsMixin, TestCasePathsMixin):
    def __init__(self, test_case: TestCase, execution_path: Path = None):
        self._test_case = test_case
        if execution_path is not None:
            self._execution_path = execution_path
        else:
            self._execution_path = self.cwd / f"{self._test_case.name}_{timestamp()}"

    @property
    def test_case(self) -> TestCase:
        return self._test_case

    @property
    def execution_path(self) -> Path:
        return self._execution_path

    @property
    def implementation_path(self) -> Path:
        return self.get_test_implementation_path(
            procedure_name=self.test_case.procedure_name
        )

    @property
    def shell_library(self) -> Path:
        return self.get_shell_lib_entry_point()

    @property
    def external_repos_base_path(self) -> Path:
        return self.cwd

    @property
    def starter(self) -> Path:
        return self.get_starter()

    @property
    def test_entry_point(self) -> Path:
        return self.get_test_entry_point(self.test_case.procedure_name)

    @property
    def module_loads_entry_point(self) -> Path:
        return self.get_load_modules_script()

    @property
    def source_dir(self) -> Path:
        return self.get_source_path()

    @property
    def log_dir(self) -> Path:
        return self.get_log_dir()

    @property
    def work_dir(self) -> Path:
        return self.get_work_dir()

    @property
    def out_dir(self) -> Path:
        return self.get_out_dir()

    def get_test_execution_structure(self) -> Dict[str, Path]:
        return {
            # paths related to rift and user cwd
            "SHELL_LIB": self.shell_library,
            "TEST_DIR": self.implementation_path,
            # paths related to specific test execution
            "SOURCE_DIR": self.get_source_path(),
            "LOG_DIR": self.get_log_dir(),
            "WORK_DIR": self.get_work_dir(),
            "OUT_DIR": self.get_out_dir(),
        }

    def get_paths_to_append_to_env_path(self):
        return [
            self.bin_dir,
            self.implementation_path,
        ]
