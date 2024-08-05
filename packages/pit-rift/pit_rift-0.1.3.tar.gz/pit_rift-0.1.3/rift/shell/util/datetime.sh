#!/usr/bin/env bash

#######################################
# Calculate the date by adding or subtracting a specified number of days.
#
# Usage:
#   dt::date_calc <date> <delta> [date_format]
#
# Parameters:
#   - $1: The base date in the format specified by 'date_format'.
#   - $2: The number of days to add (positive) or subtract (negative) from the base date.
#   - $3: (Optional) The format of the output date. Defaults to "%Y%m%d".
#
# Returns:
#   The calculated date based on the provided inputs.
#
# Examples:
#   dt::date_calc "20220125" 7              # Adds 7 days to the date.
#   dt::date_calc "20220125" -3 "%Y-%m-%d"  # Subtracts 3 days and outputs in a custom format.
#######################################
function dt::date_calc() {
    local date=${1}
    local delta=${2}
    local date_format=${3:-"%Y%m%d"}

    if [ "$(uname)" == "Linux" ]; then
        date +"${date_format}" --date="${date} ${delta} day"
    elif [ "$(uname)" == "Darwin" ]; then
        date -j -f "%Y%m%d" -v "${delta}d" "$date" +"$date_format"
    fi
}

#######################################
# Calculate the difference in days between two dates.
#
# Usage:
#   dt::date_diff <reference_date> <compare_date>
#
# Parameters:
#   - reference_date: The reference date in a format recognized by the 'date' command.
#   - compare_date: The date to compare with the reference date in the same format.
#
# Returns:
#   The difference in days between the reference_date and compare_date.
#
# Example:
#   dt::date_diff "20220120" "20220125"  # Outputs the difference as the number of days.
#######################################
function dt::date_diff() {
    local reference_date=$1
    local compare_date=$2

    echo $((($(date -d "${reference_date}" +%s) - $(date -d "${compare_date}" +%s))/86400))
}

# Exporting functions
export -f dt::date_diff
export -f dt::date_calc
