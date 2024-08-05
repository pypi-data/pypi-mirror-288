#!/usr/bin/env bash

#######################################
# Function for logging messages with timestamp and source information.
#
# Usage:
#   __logging <log_level> <msg>
#
# Parameters:
#   - $1: The log level, such as INFO, WARNING, ERROR, etc.
#   - $2: The message to be logged.
#
# Example:
#   __logging "INFO" "This is an informational message."
#
# Output Format:
#   [Timestamp] - [ScriptName.FunctionName] - Log_Level: Log_Message
#
# Dependencies:
#   - Requires 'date' command for timestamp.
#
# Author:
#   Antonio Mariani
#######################################
__logging() {
    local log_level="${1}"
    shift
    local msg=("${@}")

    local func_name="${FUNCNAME[2]:-unknown}"

    echo 1>&2 "[$(date "+%Y-%m-%dT%H:%M:%SZ")] - ${log_level} - ${func_name}: " "${msg[@]}"
}

logger::debug() {
    local msg=("${@}")
    local this_level=5
    [ "${this_level}" -le "${LOGGER_LEVEL}" ] && __logging 'DEBUG' "${msg[@]}"
    return 0
}


logger::info() {
    local msg=("${@}")
    local this_level=4

    [ "${this_level}" -le "${LOGGER_LEVEL}" ] && __logging 'INFO' "${msg[@]}"
    return 0
}

logger::warning() {
    local msg=("${@}")
    local this_level=3

    [ "${this_level}" -le "${LOGGER_LEVEL}" ] && __logging 'WARNING' "${msg[@]}"
    return 0
}

logger::error() {
    local msg=("${@}")
    local this_level=2

    [ "${this_level}" -le "${LOGGER_LEVEL}" ] && __logging 'ERROR' "${msg[@]}"
    return 0
}

logger::critical() {
    local msg=("${@}")
    local this_level=1

    [ "${this_level}" -le "${LOGGER_LEVEL}" ] && __logging 'CRITICAL' "${msg[@]}"
    return 0
}

logger::set_level() {
    local level=${1}
    export LOGGER_LEVEL="${level}"
    return 0
}

# set default log level
logger::set_level 4

# exporting functions
export -f __logging
export -f logger::debug
export -f logger::info
export -f logger::warning
export -f logger::error
export -f logger::critical
