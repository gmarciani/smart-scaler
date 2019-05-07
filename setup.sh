#!/usr/bin/env bash

# Usage:
# setup [install|uninstall] [metacontroller|controller]

OPERATION=$1
OBJECT=$2

HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

METACONTROLLER_NAMESPACE=metacontroller
METACONTROLLER_RBAC=https://raw.githubusercontent.com/GoogleCloudPlatform/metacontroller/master/manifests/metacontroller-rbac.yaml
METACONTROLLER_YAML=https://raw.githubusercontent.com/GoogleCloudPlatform/metacontroller/master/manifests/metacontroller.yaml

SMARTSCALER_CONTROLLER_YAML="${HOME_DIR}/controllers/smartscaler-controller.yaml"
SMARTSCALER_LOGIC_PY="${HOME_DIR}/controllers/hooks/smartscaler-hooks-logic.py"
SMARTSCALER_HOOK_DEPLOYMENT_YAML="${HOME_DIR}/controllers/hooks/smartscaler-hook-deployment.yaml"
SMARTSCALER_HOOK_SERVICE_YAML="${HOME_DIR}/controllers/hooks/smartscaler-hook-service.yaml"

SMARTSCALER_SERVICE_NAME="smartscaler-controller"
SMARTSCALER_DEPLOYMENT_NAME="smartscaler-controller"
SMARTSCALER_CONFIGMAP_NAME="smartscaler-controller"
SMARTSCALER_COMPOSITECONTROLLER_NAME="smartscaler-controller"

function printUsage {
    echo "bash setup.sh [install|uninstall] [metacontroller|controller]"
}

function installMetacontroller {
    echo "Installing Metacontroller"
    kubectl create namespace ${METACONTROLLER_NAMESPACE}
    kubectl apply -f ${METACONTROLLER_RBAC}
    kubectl apply -f ${METACONTROLLER_YAML}
}

function uninstallMetacontroller {
    echo "Uninstalling Metacontroller"
}

function installController {
    echo "Installing Smart Scaler Controller"
    kubectl apply -f ${SMARTSCALER_CONTROLLER_YAML}
    kubectl create configmap ${SMARTSCALER_CONFIGMAP_NAME} --from-file=${SMARTSCALER_LOGIC_PY}
    kubectl apply -f ${SMARTSCALER_HOOK_DEPLOYMENT_YAML}
    kubectl apply -f ${SMARTSCALER_HOOK_SERVICE_YAML}
}

function uninstallController {
    echo "Uninstalling Smart Scaler Controller"
    kubectl delete service ${SMARTSCALER_SERVICE_NAME}
    kubectl delete deployment ${SMARTSCALER_DEPLOYMENT_NAME}
    kubectl delete configmap ${SMARTSCALER_CONFIGMAP_NAME}
    kubectl delete compositecontroller ${SMARTSCALER_COMPOSITECONTROLLER_NAME}
}

if [[ -z ${OPERATION} ]] | [[ -z ${OBJECT} ]]; then
    printUsage
    exit -1
fi

if [[ ${OPERATION} = "install" ]]; then
    if [[ ${OBJECT} = "metacontroller" ]]; then
        installMetacontroller
    elif [[ ${OBJECT} = "controller" ]]; then
        installController
    fi
elif [[ ${OPERATION} = "uninstall" ]]; then
    if [[ ${OBJECT} = "metacontroller" ]]; then
        uninstallMetacontroller
    elif [[ ${OBJECT} = "controller" ]]; then
        uninstallController
    fi
fi



