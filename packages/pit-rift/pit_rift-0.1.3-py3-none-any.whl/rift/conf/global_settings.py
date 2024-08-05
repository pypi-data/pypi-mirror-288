########################
# TEST STRUCTURE
########################

# where configuration file are expected to be put
TEST_CASES_BASE_DIR = "test_cases"
# where expect to find the test implementation
TESTS_BASE_DIR = "tests"

# Directory names
REFERENCE_TEST_DIR = "CMCC_local"  # used to redirect procedure definition and test execution in this directory
BASEDIR_PROCEDURES = (
    "tests"  # in CMCC_local: directory where to put the test procedure directories
)
SHELL_LIB_DIRNAME = "shell"  # contains shell libraries imported by starter
PYTHON_LIB_DIRNAME = "lib"  # contains python libraries
BIN_DIRNAME = "bin"


# Script names
LOAD_MODULES = "load_modules.sh"  # used to load the modules declared in the test case
TEST_ENTRY_POINT = "main.sh"  # the starting point of the test
RIFT_ENTRY_POINT = "start.sh"  # the first script called by the rift
SHELL_UTILS = "utils.sh"  # the first script called by the manager

########################
# MOCK
########################
MOCK_PROCEDURE_NAME = "mock_test_procedure"
MOCK_MAIN = "main.sh"
MOCK_TEST_CASE = "test_case.ini"

########################
# LOG
########################

# The callable to use to configure logging
LOGGING_CONFIG = "logging.config.dictConfig"

# Custom logging configuration.
LOGGING = {}

DEBUG = False
