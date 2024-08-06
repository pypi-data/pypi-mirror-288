#!/usr/bin/env bash

exec_task_usage() {
cat 2>&1 << HELP
    Usage: exec_task <cmd> [OPTIONS]

    OPTIONS
        -m, --mem <memory>          Sets a memory limit for all the processes that belong to the job.
        -r, --runtime <runtime>     Sets the runtime limit of the job.
        -q, --queue                 Submits the job to specified queue.
        -j, --jobname <jobname>     Assigns the specified name to the job.
        -w, --wait                  Submits a job and waits for the job to complete. Sends job status messages to the terminal.
        -l, --log <log>             Path of the directory where to write LSF/SLURM log files.
        -h, --help                  Show this help message and exit.
HELP
exit 0
}

exec_task() {
    local opts mem wait runtime jobname log queue
    opts=$(getopt -o m:r:j:l:q:hw --long mem:,runtime:,jobname:,log:,queue:,help,wait -- "$@") || exec_task_usage

    eval set -- "${opts}"
    # Process options
    while :; do
        case "$1" in
            -m|--mem)
                mem="${2}"
                shift 2
                ;;
            -w|--wait)
                wait="true"
                shift
                ;;
            -r|--runtime)
                runtime="${2}"
                shift 2
                ;;
            -j|--jobname)
                jobname="${2}"
                shift 2
                ;;
            -l|--log)
                log="${2}"
                shift 2
                ;;
            -q|--queue)
                queue="${2}"
                shift 2
                ;;
            -h|--help)
                exec_task_usage
                ;;
            --)
                shift
                break
                ;;
            *)
                printf "Unexpected option: %s\n" "${1}"
                exec_task_usage
                ;;
        esac
    done

    mem="${mem:-"${SUBMIT_MEM_LIMIT}"}"
    runtime="${runtime:-"${SUBMIT_RUN_TIME}"}"
    queue="${queue:-"${SUBMIT_QUEUE}"}"
    log="${log:-"${SUBMIT_LOG_DIR}"}"
    wait="${wait:-""}"
    jobname="${jobname:-""}"

    # Check if the required command is provided
    [ -z "$1" ] && exec_task_usage
    local cmd="$1"

    # --id provide fundamental info to submit a job like project id (LSF) or account name (SLURM)
    local options=('--id')
    # Optional
    [ -n "$wait" ] && options+=("--wait")
    [ -n "$jobname" ] && options+=("--job_name $jobname")
    [ -n "$runtime" ] && options+=("--run_time $runtime")

    # Mandatory
    [ -z "$mem" ] && { echo "Memory option not defined - MYE_MEM_REQUEST can be used"; exec_task_usage; }
    [ -z "$log" ] && { echo "Log directory not defined - LOG_DIR can be used"; exec_task_usage; }
    [ -z "$queue" ] && { echo "Please select a queue - MYE_QUEUES can be used"; exec_task_usage; }
    options+=("-m $mem")
    options+=("--log_dir $log" "-e aderr_%J" "-o adout_%J")

    # Submission
    local submission_parameter submission_cmd
    submission_parameter="$(job_scheduler_resolver ${options[@]})"
    submission_cmd=$(job_scheduler_resolver --cmd)

    ${submission_cmd} ${submission_parameter} ${cmd}
}

export -f exec_task_usage
export -f exec_task
