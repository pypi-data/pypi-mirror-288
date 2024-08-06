import logging
from pathlib import Path

from rift import conf as settings
from rift.factories.test_case_factory import get_test_case
from rift.paths import PathManager

logger = logging.getLogger("rift")


def initialize_test_case(test_case_config: Path) -> None:
    """
    Initialize a test case if it doesn't exist yet'

    Args:
        test_case_config: Path where to initialize the test case
        execution_dir: Path where to execute the test case
    """
    if test_case_config.exists():
        logger.info(
            "Test case %s already exists", test_case_config.absolute().as_posix()
        )
        return
    test_name = test_case_config.stem

    ########################
    # TEST CASE
    ########################
    test_case_content = settings.MOCK_CONFIG
    test_case_content = test_case_content.replace(
        settings.TEST_NAME_PLACEHOLDER,
        test_name,
    )
    test_case_config.parent.mkdir(parents=True, exist_ok=True)
    test_case_config.write_text(test_case_content)

    ########################
    # TEST IMPLEMENTATION
    ########################
    test_case = get_test_case(test_case_config)
    path_manager = PathManager(test_case)
    main_path = path_manager.test_entry_point
    if main_path.exists():
        logger.info(f"Test implementation already exists: {main_path}")
        return

    main_path.parent.mkdir(parents=True, exist_ok=True)
    main_mock_content = settings.MOCK_ENTRY_POINT_CONTENT
    main_path.write_text(main_mock_content)
