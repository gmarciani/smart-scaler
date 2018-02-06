#!/bin/bash

##
# Launch the specified service
#
# @Usage: bash up.sh [serviceName] [mode]
#         * *serviceName* can be
#           * agents_manager
#           * api_gateway
#           * repo_manager
#           * kubernetes_simulator
#           * redis_simulator
#         * *mode* can be
#           * local
#           * kubernetes
##

SERVICE=$1
MODE="local"

SERVICE_DIR="services/${SERVICE}"

if [ -z "SERVICE_DIR" ]; then
    echo "Usage: $(basename $0) service" >&2
    exit 1
fi

kubectl create -f "${SERVICE_DIR}/deployment.yaml"
kubectl create -f "${SERVICE_DIR}/service.yaml"
