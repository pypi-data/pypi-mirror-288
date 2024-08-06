# RIFT

RIFT stands for - pa**R**ametrized **I**ntegration testing **F**ramework **T**ool.
It's an integration test framework that focuses its attention to the parametrization and standardization of test procedure.


![Python](https://img.shields.io/badge/Python->3.10-blue.svg)
[![Anaconda](https://img.shields.io/badge/conda->22.11.1-green.svg)](https://anaconda.org/)
[![Pip](https://img.shields.io/badge/pip->19.0.3-brown.svg)](https://pypi.org/project/pip/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
![Tests](https://img.shields.io/badge/coverage-76%25-green)

## Installation

### Using mamba or conda (recommended)

```shell
mamba create -n riftenv
mamba activate riftenv
mamba install pit-rift
```

### Using pip

```bash
pip install pit-rift
```

## Usage

[How to create a test](#how-to-create-a-test) | [Documentation](doc/README_test_case.md)

```shell
rift <path_to_test_case> [-v VERBOSE_LEVEL] [-w WORK_DIR] [-i] [-h]
```
### Positional Argument

* `test_case`: Path to the test case (in ini format) to exec.

### Optional Arguments

* `-v VERBOSE_LEVEL`: Optional. Verbose level from 1 (CRITICAL) to 5 (DEBUG). Default is 4 (INFO).
* `-w WORK_DIR`: To change the test working directory. Default is ini_test_case_YYYYMMDDTHHmmss.
* `-i`: If the test case doesn't exist, create it
* `-h, --help`: Show this help message and exit.


### Usage Requirements

If we indicate with `<my_test_case>` a test case to execute, the following requirements must be satisfied:

1. The command `rift` must be executed in a directory which contains `tests`
2. The test implementation must be located in: `tests/<procedure_name>`, 
    where `<procedure_name>` is the value of `<my_test_case>[EXEC]test_procedure`

It's a good practice to save all test cases in a directory called `test_cases`

## How to create a test

To create a test case **my_test_case**, run the commands:

```shell
rift test_cases/my_test_case.ini  -i
```

After the execution, your working directory will appear like this:

```shell
CWD/
├── my_test_case.ini_20240105T165240
│ ├── log
│ │ ├── my_test_case.ini
│ │ ├── pid
│ │ └── test.log
│ ├── out
│ └── work
├── my_test_case.ini
└── tests
    └── my_test_case
        └── main.sh
```

Expected output:

```shell
(base) [am09320@juno CMCC_local]$ rift test_cases/my_test_case.ini  -i
[2024-01-05T17:08:30Z] - INFO - mock.create_test: Init test case: test_cases/my_test_case.ini
[2024-01-05T17:08:30Z] - INFO - mock.init_test_procedure: Mkdir procedure: /work/opa/am09320/dev/DevOpsEnv/CMCC_local/tests/mock_test
[2024-01-05T17:08:30Z] - INFO - mock.init_test_procedure: Copy /work/opa/am09320/dev/DevOpsEnv/dev_refactoring/conf/main.sh to /work/opa/am09320/dev/DevOpsEnv/CMCC_local/tests/mock_test
[2024-01-05T17:08:30Z] - INFO - mock.init_test_case: Mkdir test_cases
[2024-01-05T17:08:30Z] - INFO - mock.init_test_case: Copy /work/opa/am09320/dev/DevOpsEnv/dev_refactoring/conf/test_case.ini as test_cases/my_test_case.ini
[2024-01-05T17:08:30Z] - INFO - rift.main: Loading test case: test_cases/my_test_case.ini
...
[2024-01-05T17:08:30Z] - INFO - scheduler.exec: EXECUTION START
INFO Loading modules

INFO Starting test case
Hello World!
Variable declared into test_case: This is a test
[2024-01-05T17:08:30Z] - INFO - scheduler.exec: EXECUTION_DONE
```

Once the test has been created, the parameter `-i` can be omitted

### Long runs
If the running time of a test is too long (due to the running time or the waiting time of a job),
it's possible to exec rift in background using `nohup`:

```shell
nohup rift test_cases/my_test_case.ini &> my_test_case.log &
```

---
## Authors

* **Antonio mariani** - antonio.mariani@cmcc.it

### Contributors

- **Massimiliano Drudi** - massimiliano.drudi@cmcc.it

---
## References

- What is DevOps?, Web article, https://opensource.com/resources/devops?src=devops_resource_menu1
- Is there a reproducibility crisis in Science?, Nature Video, 2016, https://www.nature.com/articles/d41586-019-00067-3
- Keyes DE, McInnes LC, Woodward C, et al. Multiphysics simulations: Challenges and opportunities. The International
  Journal of High Performance Computing Applications. 2013;27(1):4-83. https://doi.org/10.1177/1094342012468181
- Theorists and experimentalists must join forces, Nature Editorial,
  2021, https://www.nature.com/articles/s43588-021-00082-3
- But is the code (re)usable?, Nature Editorial, 2021, https://www.nature.com/articles/s43588-021-00109-9
- Zebula Sampedro, Aaron Holt, and Thomas Hauser. 2018. Continuous Integration and Delivery for HPC: Using Singularity
  and Jenkins. In Proceedings of the Practice and Experience on Advanced Research Computing (PEARC '18). Association for
  Computing Machinery, New York, NY, USA, Article 6, 1–6. https://doi.org/10.1145/3219104.3219147
- Dong H. Ahn, Allison H. Baker, Michael Bentley, Ian Briggs, Ganesh Gopalakrishnan, Dorit M. Hammerling, Ignacio
  Laguna, Gregory L. Lee, Daniel J. Milroy, and Mariana Vertenstein. 2021. Keeping science on keel when software moves.
  Commun. ACM 64, 2 (February 2021), 66–74. https://doi.org/10.1145/3382037
- National Academies of Sciences, Engineering, and Medicine. 2019. Reproducibility and Replicability in Science.
  Washington, DC: The National Academies Press. https://doi.org/10.17226/25303.
- Geyer, B., Ludwig, T. & von Storch, H. Limits of reproducibility and hydrodynamic noise in atmospheric regional
  modelling. Commun Earth Environ 2, 17 (2021). https://doi.org/10.1038/s43247-020-00085-4
