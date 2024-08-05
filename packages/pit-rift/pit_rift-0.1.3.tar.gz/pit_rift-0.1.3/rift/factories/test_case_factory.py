from pathlib import Path

import rift.conf as settings
from rift.model import TestCase


def get_test_case(test_case_config: Path) -> TestCase:
    test_case_content: dict = settings.read_config(test_case_config.resolve(), keep_sections=True)
    git_keys_section = [k for k in test_case_content.keys() if k.startswith('GIT_')]

    # default value if no repos in test_case_config
    git_sections = []
    for k in git_keys_section:
        git_sections.append(test_case_content.pop(k))

    test_case_content['REPOSITORIES'] = git_sections
    return TestCase(path=test_case_config, **test_case_content)
