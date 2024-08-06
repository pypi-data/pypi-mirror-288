#!/bin/bash

SHELL_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ) # dirname $0 = /bin/env if source this script
UTIL_DIR="${SHELL_DIR}/util"

# DON'T CHANGE THE ORDER OF log.sh error.sh
EXT_LIBRARIES=("log.sh" "datetime.sh" "submit.sh" "deprecated.sh")

for lib_name in "${EXT_LIBRARIES[@]}"; do
    lib_to_import="${UTIL_DIR}/${lib_name}"
    if [ ! -f "${lib_to_import}" ]; then
        echo 1>&2 "File '${lib_to_import}' doesn't exists"
    else
        # shellcheck disable=SC1090
        . "${lib_to_import}"
    fi
done

