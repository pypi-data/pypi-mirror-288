#!/bin/bash

rootPid="$1"

_safeKillProc() {
    local pid=$1
    if ! kill -9 "${pid}" > /dev/null 2>&1; then
        echo "Process with pid: ${pid} is already terminated"
    fi
}

_listDescendantsPid () {
    local rootPid="$1"
    local children; children=$(ps -o pid= --ppid "${rootPid}")

    for pid in ${children}; do
        _listDescendantsPid "$pid"
    done

    echo "$children"
}

for pid in $(_listDescendantsPid "${rootPid}"); do
    echo "Killing process with pid: ${pid}"
    _safeKillProc "${pid}"
done

echo "Killing root process with pid: ${rootPid}"
_safeKillProc "${rootPid}"
