#!/bin/bash

##
# Run Docker containers.
#
# @Usage: bash docker.sh
##

HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVICES_DIR="${HOME_DIR}/services"

##
# SERVICE: API GATEWAY
##
API_GATEWAY_CONTAINER="api_gateway"
API_GATEWAY_IMAGE="smart_scaler_api_gateway"
API_GATEWAY_IMAGE_VERSION="1.0.0"
API_GATEWAY_DOCKER_PATH="${SERVICES_DIR}/api_gateway"
API_GATEWAY_PORT=18001

##
# SERVICE: AGENTS MANAGER
##
AGENTS_MANAGER_CONTAINER="agents_manager"
AGENTS_MANAGER_IMAGE="smart_scaler_agents_manager"
AGENTS_MANAGER_IMAGE_VERSION="1.0.0"
AGENTS_MANAGER_DOCKER_PATH="${SERVICES_DIR}/agents_manager"
AGENTS_MANAGER_PORT=18002

##
# SERVICE: REDIS
##
REDIS_SIMULATOR_CONTAINER="redis_simulator"
REDIS_SIMULATOR_IMAGE="smart_scaler_redis_simulator"
REDIS_SIMULATOR_IMAGE_VERSION="1.0.0"
REDIS_SIMULATOR_DOCKER_PATH="${SERVICES_DIR}/redis_simulator"
REDIS_SIMULATOR_PORT=18003

##
# SERVICE: KUBERNETES
##
KUBERNETES_SIMULATOR_CONTAINER="kubernetes_simulator"
KUBERNETES_SIMULATOR_IMAGE="smart_scaler_kubernetes_simulator"
KUBERNETES_SIMULATOR_IMAGE_VERSION="1.0.0"
KUBERNETES_SIMULATOR_DOCKER_PATH="${SERVICES_DIR}/kubernetes_simulator"
KUBERNETES_SIMULATOR_PORT=18004

##
# BUILD
##
build ${API_GATEWAY_IMAGE}, ${API_GATEWAY_IMAGE_VERSION}, ${API_GATEWAY_DOCKER_PATH}
build ${AGENTS_MANAGER_IMAGE}, ${AGENTS_MANAGER_IMAGE_VERSION}, ${AGENTS_MANAGER_DOCKER_PATH}
build ${REDIS_SIMULATOR_IMAGE}, ${REDIS_SIMULATOR_IMAGE_VERSION}, ${REDIS_SIMULATOR_DOCKER_PATH}
build ${KUBERNETES_SIMULATOR_IMAGE}, ${KUBERNETES_SIMULATOR_IMAGE_VERSION}, ${KUBERNETES_SIMULATOR_DOCKER_PATH}

##
# PULL
##
#pull ${REDIS_IMAGE}:${REDIS_IMAGE_VERSION}

##
# RUN
##
run ${API_GATEWAY_IMAGE} ${API_GATEWAY_IMAGE_VERSION} ${API_GATEWAY_CONTAINER} ${API_GATEWAY_PORT}


function build () {
    image=$1
    version=$2
    path=$3
    docker build -t ${image}:${version} ${path}
}

function pull () {
    image=$1
    version=$2
    docker pull ${image}:${version}
}

function run () {
    image=$1
    version=$2
    container=$3
    port=$4
    docker run ${image}:${version} --name ${container} -d -p ${port}:${port}
}