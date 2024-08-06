# RIFT Framework Documentation

## Introduction

The RIFT framework, puts its focus in the procedure re-usability,
providing the necessary execution information via parameters.

It's composed by:

* **Test case**: It's a configuration file in .ini format which contains the necessary information for executing a test.
  Each test case, represents a well specific scenario that must be tested using a general procedure.
* **Test procedure**: Parameterized code that runs the test with the parameters and environment provided by a test case

## Test case

### Template

Here is a template that can be used as base to build your own test case:

```ini
[Environment]

MY_VAR = value1
...
MY_VARX = Another value

[Exec]
test_procedure = mock_test_procedure
;write as module1 module2 ... moduleX -> automatic loaded before to call the test procedure
modules =
;if defined, the conda environment is automatic loaded before to call the test procedure
conda_env =

;the git sections are optionals - it is possible to declare as much section as you want
[GIT_REPO1]
name = REPO1
url = SSH_GIT_URL
; branch or tag to download - mandatory
branch = GIT_BRANCH

[GIT_REPOX]
;cloned as CMCC_local/<name>
name = REPOX
url = SSH_GIT_URL
; branch or tag to download - mandatory
branch = GIT_BRANCH
```

### Example

Here is a real example of a working test case (from [quick-start example](../README.md#quick-start)):

```shell
[Environment]

MY_VAR = This is a test
MY_VAR2 = Another custom variable


[Exec]

test_procedure = mock_test_procedure
# no modules to load
modules =
# no conda env to load
conda_env =
```

### Section Environment

In the environment section:

* declaring all variables needed to exec the test
* the variable name is case-sensitive: `VAR != var`
* all variables will be automatically exported by the test framework before to run the test procedure
* no limit in the number of variables that ca be declared
* a variable can refer to another variable declared previously into the same file using the bash syntax: 
```
var1 = MY_VALUE
;set var2 as MY_VALUE_extend
var2 = ${var1}_extended
```

### Section Exec
In this section, is reported some information needed for the test execution:

* **test_procedure**: name of the directory in `CMCC_local/tests` which contains the main.sh to start the test
* **modules**: list of module name that will be loaded using te command `module load` before to run the test procedure (ignored if empty) 
* **conda_env**: name of the conda env to load before to run the test procedure (ignored if empty)


## Test Procedure
### Definition

A test procedure is a collection of parametrized procedures which are in charge to exec the test. 
It's composed by:

* **main.sh**: it's the starting point called by the test framework
* any other executable script necessary for the test execution: **the test procedure path will be added to the PATH**, this means that it is possible to use into the test case any script that the test needs


### Global Environment
Here is a list of global variables exported by the test framework that can be used in the test implementation:

- **SOURCE_DIR**: The parent directory of CMCC_local
- **TEST_DIR**: The test procedure dir: `CMCC_local/tests/<test_case>`
- **LOG_DIR**: `<test_case>_YYYYMMDDTHHmmss/log`
- **WORK_DIR**: `<test_case>_YYYYMMDDTHHmmss/work`
- **DATA_DIR**: `<test_case>_YYYYMMDDTHHmmss/data`
- **OUT_DIR**: `<test_case>_YYYYMMDDTHHmmss/out`
- **STATUS_DIR**: `<test_case>_YYYYMMDDTHHmmss/status`

### Global Function

The bash libraries introduced with old versions of rift,
are still available, but they will be removed in the next releases.
The libraries will print a warning message to alert the users.

Currently, the test framework, provides two type of libraries:

* [Logging](#logging)
* [Submission](#submission)

#### Logging
It is a bash implementation of the python logging library [[1]](#1-logging-facility-for-python):

* `logger::debug`
* `logger::info`
* `logger::warning`
* `logger::error`
* `logger::critical`

For each function, the printed format is:

```shell
[YYYY-MM-DDTHH:mm:ssZ] - <LEVEL> - <FUNC_NAME>: <MSG>
```
where LEVEL is: DEBUG, INFO, WARNING, ERROR, CRITICAL

#### Submission

A function is available to submit a job to LSF or SLURM with a general interface.

```shell
Usage: exec_task <cmd> [OPTIONS]

OPTIONS
    -m, --mem <memory>          Sets a memory limit for all the processes that belong to the job.
    -r, --runtime <runtime>     Sets the runtime limit of the job.
    -q, --queue                 Submits the job to specified queue.
    -j, --jobname <jobname>     Assigns the specified name to the job
    -w, --wait                  Submits a job and waits for the job to complete. Sends job status messages to the terminal
    -l, --log <log>             Path of the directory where to write LSF/SLURM log files
    -h, --help                  Show this help message and exit
```

As an alternative, it is possible to pass some parameter directly from variables declared into the test case:

* **SUBMIT_MEM_LIMIT**: Sets a memory limit for all the processes that belong to the job.
* **SUBMIT_RUN_TIME**: Sets the runtime limit of the job.
* **SUBMIT_QUEUE**: Submit the job to specified queue.
* **SUBMIT_LOG_DIR**: Path of the directory where to write LSF/SLURM log files

## Test Execution

If we indicate with `<cmcc_local>` the path of CMCC_local which contains the test,
to exec a test `<my_test_case>`exec the commands:

```shell
cd <cmcc_local>
rift test_cases/<my_test_case>.ini
```


## Reference

### R1. 
Logging facility for Python, [direct link](https://docs.python.org/3/library/logging.html)
