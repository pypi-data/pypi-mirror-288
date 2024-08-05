#!/usr/bin/env python

"""
This script provides an abstract interface to access the schedulers.
It provides a general access way also if the scheduler changes.
"""

__author__ = "Antonio Mariani"
__date__ = "2023/03/24"
__copyright__ = "CMCC Foundation - Euro-Mediterranean Center on Climate Change"

import subprocess
import os

LSF_SCHEDULER = "LSF"
SLURM_PARAMETER = "SLURM"

SUPPORTED_SCHEDULER = {LSF_SCHEDULER: ["bsub"], SLURM_PARAMETER: ["sbatch"]}

EMPTY_STRING = ""


def get_args():
    import argparse

    parse = argparse.ArgumentParser(description="Archiving tool")

    # General args

    parse.add_argument(
        "-c", "--cmd", action="store_true", help="Get scheduler command to submit jobs"
    )
    parse.add_argument(
        "-w", "--wait", action="store_true", help="To request waiting parameter"
    )
    parse.add_argument(
        "-ps",
        "--prios",
        action="store_true",
        help="Return a string with sequential prio_flag parameter-values",
    )
    parse.add_argument(
        "-pp",
        "--priop",
        action="store_true",
        help="Return a string with parallel prio_flag parameter-values",
    )
    parse.add_argument(
        "-i", "--id", action="store_true", help="Return a string with id info"
    )

    parse.add_argument(
        "-s",
        "--post_exec",
        type=str,
        default=None,
        help="Run command the job finishes - only LSF",
    )
    parse.add_argument(
        "-m",
        "--mem",
        type=str,
        default=None,
        help="To request memory request parameter",
    )
    parse.add_argument(
        "-t",
        "--run_time",
        type=str,
        default=None,
        help="To request jon running time parameter",
    )
    parse.add_argument(
        "-j", "--job_name", type=str, default=None, help="To request job name parameter"
    )

    parse.add_argument(
        "-e", "--err", type=str, default=None, help="Enable standard error log"
    )
    parse.add_argument(
        "-o", "--out", type=str, default=None, help="Enable standard output log"
    )
    parse.add_argument(
        "-l",
        "--log_dir",
        type=str,
        default=".",
        help="Change directory where store log files",
    )
    parse.add_argument("-q", "--queue", type=str, default=None, help="Set queue")
    parse.add_argument("-n", "--ntask", type=str, default=None, help="Number of task")

    return parse.parse_args()


def get_optional_attributes(key, dictionary: dict):
    value = dictionary.get(key, None)

    if value is not None and len(value) != 0:
        return value
    else:
        return None


def build_priority(app, sla):
    # sla and app must be present MANDATORY together
    if sla is not None and app is None:
        raise ValueError(f"ERROR sla is defined but app value is not defined")
    elif sla is None and app is not None:
        raise ValueError(f"ERROR sla is not defined but app value is defined")
    elif app is not None and sla is not None:
        priority_parameter = f"-sla {sla} -app {app}"
    else:
        priority_parameter = EMPTY_STRING
    return priority_parameter


class SchedulerResolver:
    def __init__(self):
        self._job_scheduler = None
        self._scheduler_cmd = None
        self._env: dict = os.environ

        self._load_scheduler_info()

    def _load_scheduler_info(self, verbose: bool = False):
        stdout = None if verbose else subprocess.PIPE
        stderr = None if verbose else subprocess.PIPE

        for scheduler, cmd_list in SUPPORTED_SCHEDULER.items():
            for cmd in cmd_list:
                result = subprocess.run(
                    [f"which {cmd} 2>/dev/null"],
                    stdout=stdout,
                    stderr=stderr,
                    text=True,
                    shell=True,
                )
                if result.returncode == 0:
                    if verbose:
                        print(f"Found scheduler: {scheduler}")
                    self._job_scheduler = scheduler
                    self._scheduler_cmd = cmd
                    break
        if self._job_scheduler is None:
            raise Exception("No scheduler has been found on the current machine")

    def get_cmd(self):
        return self._scheduler_cmd

    def get_post_exec_parameter(self, cmd_to_exec: str):
        if self._job_scheduler == SLURM_PARAMETER:
            return None
        elif self._job_scheduler == LSF_SCHEDULER:
            return f'-Ep "{cmd_to_exec}"'

    def get_wait_parameter(self):
        if self._job_scheduler == SLURM_PARAMETER:
            return "-W"
        elif self._job_scheduler == LSF_SCHEDULER:
            return "-K"

    def get_runtime_limit_parameter(self, r_limit):
        if self._job_scheduler == SLURM_PARAMETER:
            return f"-t {r_limit}"
        elif self._job_scheduler == LSF_SCHEDULER:
            return f"-W {r_limit}"

    def get_job_name_parameter(self, job_name):
        return f"-J {job_name}"

    def get_mem_request(self, memory_to_request):
        if self._job_scheduler == SLURM_PARAMETER:
            return f"--mem={memory_to_request}"
        elif self._job_scheduler == LSF_SCHEDULER:
            return f'-R "rusage[mem={memory_to_request}]"'

    def get_id(self):
        """LSF needs ID_PROJECT and SLURM needs ACCOUNT parameter, otherwise the job will be refused"""
        if self._job_scheduler == SLURM_PARAMETER:
            account_slurm = os.environ.get("MYE_ACCOUNT", None)
            if account_slurm is None:
                raise ValueError(
                    f"ERROR In {SLURM_PARAMETER} is mandatory the parameter MYE_ACCOUNT"
                )
            else:
                return f"-A {account_slurm}"
        elif self._job_scheduler == LSF_SCHEDULER:
            id_project = os.environ.get("MYE_LSF_Project", None)
            if id_project is None:
                raise ValueError(
                    f"ERROR In {LSF_SCHEDULER} is mandatory the parameter MYE_LSF_Project"
                )
            else:
                return f"-P {id_project}"

    def get_sequential_priority(self):
        if self._job_scheduler == SLURM_PARAMETER:
            priority_parameter = self.get_slurm_prio()
        elif self._job_scheduler == LSF_SCHEDULER:
            sla = get_optional_attributes("MYE_SC_serial", self._env)
            app = get_optional_attributes("MYE_LSF_SAPP", self._env)
            priority_parameter = build_priority(app, sla)
        else:
            self._unknown_scheduler()

        return priority_parameter

    def get_parallel_priority(self):
        if self._job_scheduler == SLURM_PARAMETER:
            priority_parameter = self.get_slurm_prio()
        elif self._job_scheduler == LSF_SCHEDULER:
            sla = get_optional_attributes("MYE_SC", self._env)
            app = get_optional_attributes("MYE_LSF_PAPP", self._env)
            priority_parameter = build_priority(app, sla)
        else:
            self._unknown_scheduler()

        return priority_parameter

    def get_slurm_prio(self):
        """In Slurm (G100) is used only parallel priority/queue"""
        qos = get_optional_attributes("MYE_QOS", self._env)
        reservation = get_optional_attributes("MYE_RESERVATION", self._env)
        priority_parameter = EMPTY_STRING
        if qos is not None:
            priority_parameter = f"-q {qos}"
        if reservation is not None:
            if priority_parameter is None:
                priority_parameter = f"--reservation {reservation}"
            else:
                priority_parameter = f"{priority_parameter} --reservation {reservation}"
        return priority_parameter

    def get_sequential_ntask(self):
        if self._job_scheduler == SLURM_PARAMETER:
            return f"--ntasks-per-node=1 -c 1"
        if self._job_scheduler == LSF_SCHEDULER:
            return f"-n 1"

    def get_queue(self, queue):
        if self._job_scheduler == SLURM_PARAMETER:
            return f"-p {queue}"
        if self._job_scheduler == LSF_SCHEDULER:
            return f"-q {queue}"

    def get_out_log(self, log_dir, log_name):
        return f"-o {log_dir}/{log_name}"

    def get_err_log(self, log_dir, log_name):
        return f"-e {log_dir}/{log_name}"

    def _unknown_scheduler(self):
        raise Exception(f"ERROR Unknown scheduler: {self._job_scheduler}")

    def get_parallel_ntask(self, ntask):
        if self._job_scheduler == SLURM_PARAMETER:
            raise Exception(f"ERROR Not supported mode for {self._job_scheduler}")
        if self._job_scheduler == LSF_SCHEDULER:
            return f"-n {ntask}"


def build_result(input_result, new_value):
    if len(input_result) == 0:
        return new_value
    elif new_value is not None and len(new_value) > 0:
        return f"{input_result} {new_value}"
    else:
        return input_result


def main():
    args = get_args()

    cmd = args.cmd
    wait = args.wait
    sequential_priority = args.prios
    parallel_priority = args.priop
    id_job = args.id

    post_exec = args.post_exec
    mem = args.mem
    run_time = args.run_time
    job_name = args.job_name

    err_log = args.err
    out_log = args.out
    log_dir = args.log_dir  # used only with err_log/out_log
    queue = args.queue
    ntask = args.ntask

    scheduler_resolver = SchedulerResolver()
    result = EMPTY_STRING

    # No value arguments
    if cmd:
        result = build_result(result, scheduler_resolver.get_cmd())
    if wait:
        result = build_result(result, scheduler_resolver.get_wait_parameter())
    if sequential_priority:
        result = build_result(result, scheduler_resolver.get_sequential_priority())
    if parallel_priority:
        result = build_result(result, scheduler_resolver.get_parallel_priority())
    if id_job:
        result = build_result(result, scheduler_resolver.get_id())

    # Value arguments
    if post_exec:
        result = build_result(
            result, scheduler_resolver.get_post_exec_parameter(post_exec)
        )
    if mem is not None:
        result = build_result(result, scheduler_resolver.get_mem_request(mem))
    if run_time:
        result = build_result(
            result, scheduler_resolver.get_runtime_limit_parameter(run_time)
        )
    if job_name:
        result = build_result(
            result, scheduler_resolver.get_job_name_parameter(job_name)
        )

    if err_log is not None:
        result = build_result(result, scheduler_resolver.get_err_log(log_dir, err_log))
    if err_log is not None:
        result = build_result(result, scheduler_resolver.get_out_log(log_dir, out_log))
    if queue is not None:
        result = build_result(result, scheduler_resolver.get_queue(queue))
    if ntask is not None:
        if ntask == 1:
            result = build_result(result, scheduler_resolver.get_sequential_ntask())
        else:
            result = build_result(result, scheduler_resolver.get_parallel_ntask(ntask))

    print(result)


if __name__ == "__main__":
    main()
