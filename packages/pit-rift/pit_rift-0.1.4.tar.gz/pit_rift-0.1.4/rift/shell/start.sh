#!/bin/bash

################################################################################
#
# Starter used by RIFT to run the test initializing the shell environment
#
# ?? 202?
# Antonio Mariani (antonio.mariani@cmcc.it)
# First version
#
# 07 2024
# Antonio Mariani (antonio.mariani@cmcc.it)
# Improve readability
#
################################################################################

main() {
    local entry_point="${1}"
    local load_modules="${2}"

    # shellcheck source=./utils.sh
    source "${SHELL_LIB}" # load some useful common functions
    # loadModules can be the one defined by the test case or the default loading the modules declared in the ini
    # shellcheck source=./load_modules.sh
    source "${load_modules}" # load modules useful for test execution

    ########################
    # PREPARE DIRS
    ########################
    echo mkdir "${WORK_DIR}" "${LOG_DIR}" "${OUT_DIR}"
    mkdir -p "${WORK_DIR}" "${LOG_DIR}" "${OUT_DIR}"

    ########################
    # STORE START PID
    ########################
    local my_pid=$$
    echo "${my_pid}" >"${LOG_DIR}/pid"

    ########################
    # START TEST
    ########################
    echo -e "\nINFO Starting test case"
    bash "${entry_point}" &

    ########################
    # STORE TEST PID
    ########################
    local test_pid="$!"
    # save pid of testMain script
    echo "${test_pid}" >"${LOG_DIR}/pid"

    ########################
    # CHECK TEST RESULT
    ########################
    wait "${test_pid}"
    # return test exit code
    exit $?
}

main "${@}"
