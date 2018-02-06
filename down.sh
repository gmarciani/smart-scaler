#!/bin/bash

SERVICE=$1

SERVICE_DIR="services/${SERVICE}"

if [ -z "SERVICE_DIR" ]; then
    echo "Usage: $(basename $0) service" >&2
    exit 1
fi

kubectl delete -f "${SERVICE_DIR}/service.yaml"
kubectl delete -f "${SERVICE_DIR}/deployment.yaml"
