TEST_NAME_PLACEHOLDER = '{{TEST_PROCEDURE_NAME}}'

MOCK_CONFIG = """
[Environment]

MY_VAR = This is a test
MY_VAR2 = Another custom variable


[Exec]
test_procedure = {0}
; write as module1 module2 ... moduleX -> automatic loaded before to call the test procedure
modules =
; if defined, the conda environment is automatic loaded before to call the test procedure
conda_env =
    """.format(TEST_NAME_PLACEHOLDER)

MOCK_ENTRY_POINT_CONTENT = """
#! /usr/bin/env bash

#
# Author: Name Surname (mail@cmcc.it)
#
#% Common template to start a bash development
#


########################
# BASH SETTINGS
########################
set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

########################
# VARIABLES
########################
script_name=$(basename "${0}")
script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

work_dir="${WORK_DIR}"
my_var="${MY_VAR}"
readonly script_name script_dir work_dir

########################
# MAIN
########################
main() {
    cd "${work_dir}"    # where a task must work

    echo "Hello World! from ${script_dir}/${script_name}"
    echo "Variable declared into test_case: ${my_var}"
}

main "${@}"

    """
