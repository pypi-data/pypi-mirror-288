#!/usr/bin/env python

import logging
import os
import subprocess

import psutil

logger = logging.getLogger("rift")


class Scheduler:
    def __init__(self, start_script, main_procedure, load_module_script, log_dir):
        """
        :param start_script: Start test framework script
        :param main_procedure: Main script of test procedure
        :param load_module_script: Script used to load modules
        :param log_dir: Log directory
        """

        self.start_script = start_script
        self.main_procedure = main_procedure
        self.load_module_script = load_module_script
        self.log_dir = log_dir

        self._result = None

    def exec(self):
        stdout = None  # subprocess.PIPE to block stdout
        stderr = None  # subprocess.PIPE to block stderr

        logger.info(f"Starter: {self.start_script}   # added automatically")
        logger.info(f"Main: {self.main_procedure}")
        logger.info(f"Load modules: {self.load_module_script}")

        try:
            logger.info("EXECUTION START")

            print(
                f"bash {self.start_script} {self.main_procedure} {self.load_module_script}"
            )
            self._result = subprocess.run(
                [
                    f"bash {self.start_script} {self.main_procedure} {self.load_module_script}"
                ],
                stdout=stdout,
                stderr=stderr,
                text=True,
                shell=True,
            )
            logger.info("EXECUTION_DONE")
        except KeyboardInterrupt:
            logger.critical("Caught Ctrl + C, starting exit procedure...")
            pid_file = self.log_dir + "/pid"
            if os.path.exists(pid_file):  # to kill father process and all kid processes
                with open(self.log_dir + "/pid") as f:
                    pid = f.read().strip("\n")
                    kill_process_with_child(int(pid))
                logger.info("EXECUTION_DONE")
                exit(1)
            else:
                logger.error(f"Cannot find pid file: {pid_file}")

    def get_return_code(self):
        return self._result.returncode


def kill_process_with_child(root_pid):
    try:
        logger.debug(f"Root process PID: {root_pid}")
        root_process = psutil.Process(root_pid)
        logger.debug(f"Root process name: {root_process.name()}")

    except Exception as e:
        logger.debug(f"{e}")
        logger.warning(
            f"Root process with PID: {root_pid} is already terminated or does not exist, exiting..."
        )
        return

    for child in root_process.children(recursive=True):
        safe_kill(child.pid)

    logger.info("Terminating root process")
    safe_kill(root_process.pid)

    logger.info("Process termination completed successfully.")


def safe_kill(pid, timeout=5):
    try:
        logger.info(f"Kill {pid}")
        process = psutil.Process(pid)
        process.kill()
        process.wait(timeout=timeout)
    except psutil.NoSuchProcess:
        logger.debug(f"Process with PID {pid} not found.")
    except psutil.AccessDenied:  # this should never happen
        logger.error(f"Access denied when trying to terminate process with PID {pid}.")
    except psutil.TimeoutExpired:
        logger.warning(
            f"Timeout expired while waiting for process with PID {pid} to terminate."
        )
    except Exception as e:
        logger.error(f"Error occurred while terminating process with PID {pid}: {e}")
