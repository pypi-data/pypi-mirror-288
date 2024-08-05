#!/bin/bash

__deprecate_msg(){
    local func_name="${FUNCNAME[1]}"

    echo 1>&2 "WARNING The function '${func_name}' is deprecated"
}


_isDebugActive() {
    # must be the same with the one in environment.py
    DEBUG_VAR="DEBUG_IS_ACTIVE" 
    DEBUG_ACTIVE="true"
    [ "${!DEBUG_VAR}" == "${DEBUG_ACTIVE}" ] && return 0 || return 1
}

_getStrLen() {
	local inputStr=$1
	echo ${#inputStr}
}


_printSectionName() {
    local inputStr="$1"
    local count
    local strLen

    strLen="${#inputStr}"
    # read terminal width
    if [ -n "${TERM}" ] && [ ! "${TERM}" == "dumb" ] ; then
        terminalWidth=$(tput cols)
    else
        terminalWidth=30
    fi
    count=$((terminalWidth - 4))    # consider the additional character added

    spaceLenght=$((count - strLen))
    leftSpace=$((spaceLenght / 2))

    if [ ! $((spaceLenght % 2)) -eq 0 ]; then
        rightSpace="${leftSpace}"
        leftSpace=$((leftSpace + 1))
    else
        rightSpace="${leftSpace}"
    fi

    printf -v countStr '%*s' "$count"
    printf -v leftSpace '%*s' "$leftSpace"
    printf -v rightSpace '%*s' "$rightSpace"

    printf '\n\n# %s #\n' "${countStr// /-}"
    printf '# %s%s%s #\n' "${leftSpace}" "${inputStr}" "${rightSpace}"
    printf '# %s #\n\n\n' "${countStr// /-}"
}

_printInfo() {
    local inputStr=$1
    printf '# INFO: %s \n' "${inputStr}"
}

_getCallerName() {
	rawCaller="$1"
    echo "RAWCALLER: $rawCaller"
	rawCallerName=$(echo ${rawCaller} | cut -d' ' -f2)
	callerName=$(basename ${rawCallerName})
	echo "${callerName}"
}

_warnMessage() {
    local inputStr=$1
    printf '# WARNING: %s \n' "${inputStr}"
}

_errMessage() {
    local inputStr=$1
    printf '! ERROR: %s \n' "${inputStr}"
}

_printModuleName() {
    local inputStr=$1
    local count

    strLen=$(_getStrLen "${inputStr}")

    count=$((strLen + 1)) # +6 to include the length of "INFO: " 

    printf -v countStr '%*s' "$count"

    printf '\n# %s\n' "${countStr// /-}"
    printf '# %s \n' "${inputStr}"
    printf '# %s\n\n' "${countStr// /-}"
}

# _err() {
#     echo -e "[$(date +'%Y-%m-%dT%H:%M:%S%z')] ERROR: $*" >&2
# }

# Use carefully, it causes the exit of the calling script in case of errors
_errCheck() {
    local exitCode=$1
    local exitMsg=$2    # optional

    if [ ! "${exitCode}" -eq 0 ]; then
        _errMessage "${exitMsg} - exit code: ${exitCode}"
        exit 1
    fi
}

# Use carefully, it causes the exit of the calling script in case of errors
_changeDir() {
    __deprecate_msg
    local dir=$1
    cd "${dir}" || {
        _errMessage "Can't access ${dir}"
        exit 1
    }
}

_execTask() {
    __deprecate_msg
    local cmd=$1
    local jobName=${2:-task}
    local waitFlag=${3:false}

    local logDir="${LOG_DIR:?"ERROR Log directory: '$logDir' doesn't exist"}"
    local mem="${MYE_MEM_REQUEST:?"MYE_MEM_REQUEST is not defined, exiting"}"

    runTime=${MYE_WALLTIME}

    # in med_cycle test case it is used the scheduler in the cloned system, in other case the version in this repo
    which job_scheduler_resolver || exit 1

    _isDefined "${jobName}" && jobNameRequest="--job_name ${jobName}"
    [ "${waitFlag}" == "true" ] && waitRequest="--wait"
    _isDefined "${mem}" && memRequest="--mem ${mem}"
    _isDefined "${runTime}" && runTimeRequest="--run_time ${runTime}"

    schedulerPar=$(job_scheduler_resolver --id -n 1 -q ${MYE_QUEUES} --prios ${jobNameRequest} ${waitRequest} -e "aderr_%J" -o "adout_%J" --log_dir "${logDir}" ${runTimeRequest} ${memRequest})
    _errCheck $? "ERROR Unable to generate submission string"

    submissionCmd=$(job_scheduler_resolver --cmd)

    ${submissionCmd} ${schedulerPar} ${cmd}

}


_isDefined() {
    __deprecate_msg
    local varToCheck=$1
    [ -z "${varToCheck}" ] && return 1 || return 0
}

_replaceSubstring() {
    __deprecate_msg
    local inputStr=$1
    local pattern=$2
    local newValue=$3

    echo "${inputStr//${pattern}/${newValue}}"
}

_isAbsolutePath() {
    __deprecate_msg
    dir=$1
    case $dir in
    /*) return 0 ;;
    *) return 1 ;;
    esac
}

_extractDay() {
    __deprecate_msg
    local inputDate=$1  # expect date with format YYYYMMDD
    local lenInputDate

    lenInputDate=$(_getStrLen "${inputDate}")
    if [ "${lenInputDate}" == 8 ] ; then
        echo "${inputDate}" | cut -b"7 8"
    else
        _errMessage "Can't extract day from date: ${inputDate}, please use the format YYYYMMDD"
        return 1
    fi

}

_extractMonth() {
    __deprecate_msg
    local inputDate=$1  # expect date with format YYYYMMDD
    local lenInputDate

    lenInputDate=$(_getStrLen "${inputDate}")
    if [ "${lenInputDate}" == 8 ] || [ "${lenInputDate}" == 6 ]; then
        echo "${inputDate}" | cut -b"5 6"
    else
        _errMessage "Can't extract month from date: ${inputDate}, please use the format YYYYMMDD"
        return 1
    fi

}

_extractYear() {
    __deprecate_msg
    local inputDate=$1  # expect date with format YYYYMMDD
    local lenInputDate

    lenInputDate=$(_getStrLen "${inputDate}")
    if [ "${lenInputDate}" == 8 ] || [ "${lenInputDate}" == 6 ]; then
        echo "${inputDate}" | cut -b"1-4"
    else
        _errMessage "Can't extract year from date: ${inputDate}, please use the format YYYYMMDD"
        return 1
    fi
}

export -f __deprecate_msg
export -f _errCheck
export -f _changeDir
export -f _execTask
export -f _isDefined
export -f _replaceSubstring
export -f _isAbsolutePath
export -f _warnMessage
export -f _errMessage
export -f _printSectionName
export -f _getStrLen
export -f _getCallerName
export -f _printInfo
export -f _isDebugActive
export -f _printModuleName
export -f _extractDay
export -f _extractMonth
export -f _extractYear
