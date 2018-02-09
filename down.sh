#!/bin/bash

##
# Shutdown the specified service
#
# @Usage: bash down.sh [serviceName] [mode]
#         * *serviceName* can be
#           * api_gateway
#           * agents_manager
#           * kubernetes_simulator
#           * redis_simulator
#         * *mode* can be
#           * local
#           * kubernetes
##

HOME_DIR = "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CMD_KUBECTL_DELETE = kubectl delete -f

SERVICE=$1
MODE=$2

SERVICES_DIR = "${HOME_DIR}/services"
KUBERNETES_DIR = "${HOME_DIR}/kubernetes"

if [ -z "SERVICE" ]; then
    echo "Usage: $(basename $0) service mode" >&2
    exit 1
fi

if [ "${MODE}" == "local" ]; then
    echo "[smart_scaler]> local mode"
    echo PYTHONPATH = "${HOME_DIR}"
    echo python "${SERVICES_DIR}/${SERVICE}/app.py"
elif [ "${MODE}" == "kubernetes" ]; then
    echo "[smart_scaler]> kubernetes mode"
    echo ${CMD_KUBECTL_DELETE} "${KUBERNETES_DIR}/${SERVICE}/deployment.yaml"
    echo ${CMD_KUBECTL_DELETE} "${KUBERNETES_DIR}/${SERVICE}/service.yaml"
else
    echo "[smart_scaler]> Unrecognized mode ${MODE}" >&2
    exit 1
fi

exit 0

kubectl delete -f "${SERVICE_DIR}/service.yaml"
kubectl delete -f "${SERVICE_DIR}/deployment.yaml"
