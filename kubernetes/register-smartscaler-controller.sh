#!/usr/bin/env bash

kubectl apply -f smartscaler-controller.yaml
kubectl create configmap smartscaler-controller --from-file=smartscaler-sync.py
kubectl apply -f smartscaler-webhook-deployment.yaml
kubectl apply -f smartscaler-webhook-service.yaml

kubectl delete deployment smartscaler-controller
kubectl delete configmap smartscaler-controller