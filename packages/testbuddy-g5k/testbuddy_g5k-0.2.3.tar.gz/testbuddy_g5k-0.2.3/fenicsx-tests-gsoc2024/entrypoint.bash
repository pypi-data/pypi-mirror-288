#!/usr/bin/env bash

# This is not the real entrypoint. The real entrypoint is the Python
# script; however we have to first install the Python requests module
# because it is a dependency.

export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get dist-upgrade --yes && \
    apt-get install --yes python3-requests

# We launch the real entrypoint and pass along all script arguments.
for arg in "$@"; do
    if [[ $arg == --src-dir=* ]]; then
        src_dir=${arg#*=}
        "${src_dir}/entrypoint.py" "$@"
        exit $?
    fi
done
