#!/bin/bash -i

set -o errexit

NOT_DEFINED="__not_defined__"
hpc_system="${HPC_SYSTEM:-"${NOT_DEFINED}"}"
conda_env="${conda_env:-"${NOT_DEFINED}"}"
modules="${modules:-"${NOT_DEFINED}"}"

_isDefined() {
    local varToCheck=$1
    [ -z "${varToCheck}" ] && return 1 || return 0
}

module purge

echo "INFO Loading modules"
if [[ "${modules}" != "${NOT_DEFINED}" ]]; then
    IFS=' ' read -r -a modules_to_load <<< "${modules}"
    for module in "${modules_to_load[@]}"; do
        echo -e "\t- ${module}"
        module load "${module}"
    done
fi

if [[ "${conda_env}" != "${NOT_DEFINED}" ]]; then
    echo "INFO Activate conda env: ${conda_env}"
    conda activate "$conda_env"
    export -f conda
    export -f __conda_exe
    [[ "${hpc_system}" == "zeus" ]] && export -f __add_sys_prefix_to_path 2>/dev/null  # on juno this fails
    export -f __conda_activate
    export -f __conda_reactivate
    export -f __conda_hashr

fi
