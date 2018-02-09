#!/bin/bash

##
# Startup the specified service
#
# @Usage: bash up.sh [serviceName] [mode]
#         * *serviceName* can be
#           * api_gateway
#           * agents_manager
#           * kubernetes_simulator
#           * redis_simulator
#         * *mode* can be
#           * local
#           * kubernetes
##

HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVICES_DIR="${HOME_DIR}/services"
KUBERNETES_DIR="${HOME_DIR}/kubernetes"

SERVICE=$1
MODE=$2

if [ -z "SERVICE" ]; then
    echo "Usage: $(basename $0) service mode" >&2
    exit 1
fi

if [ "${MODE}" == "local" ]; then
    echo "[smart_scaler]> local mode"
    local_create ${SERVICE}
elif [ "${MODE}" == "kubernetes" ]; then
    echo "[smart_scaler]> kubernetes mode"
    echo kubernetes_create ${SERVICE}
else
    echo "[smart_scaler]> Unrecognized mode ${MODE}" >&2
    exit 1
fi

function local_create() {
    service=$1
    PYTHONPATH="${HOME_DIR}"
    python "${SERVICES_DIR}/${service}/app.py"
}

function kubernetes_create() {
    service=$1
    kubectl create -f "${KUBERNETES_DIR}/${service}/deployment.yaml"
    kubectl create -f "${KUBERNETES_DIR}/${service}/service.yaml"
}

exit 0