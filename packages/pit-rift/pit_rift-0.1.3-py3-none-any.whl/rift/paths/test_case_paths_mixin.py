from pathlib import Path

import rift.conf as settings
from rift.paths import utils


class TestCasePathsMixin:
    """
    Define the structure of directory necessary for a test case execution.
    No special rule about test cases path.
    """

    # current work dir is fundamental to reach the test implementation associated with a test case
    cwd = Path.cwd()

    @classmethod
    def get_source_path(cls):
        """Return source directory as the one which contains .git directory"""
        try:
            return utils.dot_git_parent_path(cls.cwd)
        except FileNotFoundError:
            return cls.cwd

    @classmethod
    def get_tests_base_path(cls) -> Path:
        """
        Tests base directory contains all test implementations. It is defined as:

        cwd/
        └── TESTS_BASE_DIR/

        Returns:
            Path where to find all test implementations
        """
        return cls.cwd / settings.TESTS_BASE_DIR

    @classmethod
    def get_test_implementation_path(cls, procedure_name: str) -> Path:
        """
        Test implementation contains the test entry point and all procedures
         necessary to run a test. It is defined as:

        cwd/
        └── TESTS_BASE_DIR/
            └── procedure_name/
        Args:
            procedure_name: name of the test implementation

        Returns:
            Path of the test implementation associated with the given test name
        """
        return cls.get_tests_base_path() / procedure_name

    @classmethod
    def get_test_entry_point(cls, procedure_name: str) -> Path:
        """
        The entry point is the executable called by rift starter to run the test
        cwd/
        └── TESTS_BASE_DIR/
            └── test_name/
                └── settings.TEST_ENTRY_POINT
        Args:
            procedure_name: name of the test implementation

        Returns:
            The entry point to run test_name
        """
        return cls.get_test_implementation_path(procedure_name) / settings.TEST_ENTRY_POINT
