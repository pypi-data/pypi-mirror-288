#!/usr/bin/env python
import logging
import os.path
from pathlib import Path
from typing import List

from rift.conf import environment
from rift.core import mock
from rift.core import source
from rift.factories.test_case_factory import get_test_case
from rift.core import scheduler
from rift.paths import PathManager

logger = logging.getLogger("rift")


def execute(test_case_config: Path, work_dir: Path, to_initialize: bool):
    test_case_config = test_case_config.resolve()
    ########################
    # INIT MOCK (if needed)
    ########################
    if to_initialize:
        logger.info(f"Init test case: {test_case_config}")
        mock.initialize_test_case(test_case_config)

    ########################
    # LOAD TEST CASE - PATH MANAGER
    ########################
    logger.info(f"Loading test case configuration: {test_case_config}")
    test_case = get_test_case(test_case_config)
    path_manager = PathManager(test_case, work_dir)

    ########################
    # PREPARE ENVIRONMENT
    ########################

    # append to PATH
    paths_to_export = path_manager.get_paths_to_append_to_env_path()
    for p in paths_to_export:
        environment.add_to_path(p)

    # export variables
    environ_to_export = test_case.environ()
    test_path_structure = path_manager.get_test_execution_structure()

    environment.export_dict(test_path_structure)
    environment.export_dict(environ_to_export)

    ########################
    # CLONE REPOS
    ########################
    for repo in test_case.repositories:
        source.clone(repo.url, repo.branch, dst=path_manager.external_repos_base_path)

    ########################
    # EXECUTION
    ########################
    schd = scheduler.Scheduler(
        path_manager.starter,
        path_manager.test_entry_point,
        path_manager.module_loads_entry_point,
        path_manager.log_dir,
    )
    schd.exec()
    exit_code = schd.get_return_code()
    if exit_code != 0:
        logger.error(f"TEST FAILS - exit code: {exit_code}")
        exit(exit_code)


if __name__ == "__main__":
    execute()
