#!/bin/bash

##
# Run Docker containers.
#
# @Usage: bash docker.sh
##

HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DOCKER_USER="gmarciani"
SMARTSCALERS_DOCKER_DIR="${HOME_DIR}/docker/smartscalers"

##
# SMART SCALER: CYCLIC
##
SMARTSCALER_CYCLIC_IMAGE="smartscaler_cyclic"
SMARTSCALER_CYCLIC_IMAGE_VERSION="latest"
SMARTSCALER_CYCLIC_DOCKER_PATH="${SMARTSCALERS_DOCKER_DIR}/cyclic/Dockerfile"
SMARTSCALER_CYCLIC_PORT=80

function build () {
    image=$1
    version=$2
    path=$3
    docker build -t ${image}:${version} -f ${path} ${HOME_DIR}
}

function push () {
    user=$1
    image=$2
    version=$3
    docker tag ${image} ${user}/${image}:${version}
    docker push ${user}/${image}:${version}
}

##
# BUILD
##
build ${SMARTSCALER_CYCLIC_IMAGE} ${SMARTSCALER_CYCLIC_IMAGE_VERSION} ${SMARTSCALER_CYCLIC_DOCKER_PATH}

##
# PUSH
##
docker login
push ${DOCKER_USER} ${SMARTSCALER_CYCLIC_IMAGE} ${SMARTSCALER_CYCLIC_IMAGE_VERSION}


