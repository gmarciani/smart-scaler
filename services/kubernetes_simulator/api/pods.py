from flask import Blueprint, request, jsonify
from datetime import datetime
from model.registry import PODS_DB
from model.pod import Pod
from copy import deepcopy


pods = Blueprint("pods", __name__)


@pods.route("/pods", methods=["GET"])
def get_pods():
    if not request.args:  # get all pods
        response = {
            "ts": datetime.now(),
            "pods": [vars(pod) for pod in PODS_DB.values()]
        }

    else:  # get specific pod
        pod_name = request.args["name"]
        print("pod_name: ", pod_name)
        if pod_name not in PODS_DB:
            return "Pod not found", 404

        pod = PODS_DB[pod_name]

        response = {
            "ts": datetime.now(),
            "pod": vars(pod)
        }

    return jsonify(response), 200


@pods.route("/pods", methods=["PUT"])
def create_pod():
    data = request.get_json()
    pod_name = data["name"]
    pod_replicas = int(data["replicas"]) if "replicas" in data else 1

    if pod_name in PODS_DB:
        return "Pod already exists", 400

    new_pod = Pod(pod_name, pod_replicas)
    PODS_DB[pod_name] = new_pod
    response = {
        "ts": datetime.now(),
        "created_pod": vars(new_pod)
    }

    return jsonify(response), 201


@pods.route("/pods/scale", methods=["POST"])
def scale_pod():
    data = request.get_json()
    pod_name = data["name"]
    pod_replicas = int(data["replicas"])

    if pod_name not in PODS_DB:
        return "Pod not found", 404

    scaled_pod = PODS_DB[pod_name]
    scaled_pod.replicas = pod_replicas

    response = {
        "ts": datetime.now(),
        "scaled_pod": vars(scaled_pod)
    }

    return jsonify(response), 200


@pods.route("/pods", methods=["DELETE"])
def delete_pod():
    data = request.get_json()
    pod_name = data["name"]

    if pod_name not in PODS_DB:
        return "Pod not found", 404

    deleted_pod = deepcopy(PODS_DB[pod_name])
    del PODS_DB[pod_name]

    response = {
        "ts": datetime.now(),
        "deleted_pod": vars(deleted_pod)
    }

    return jsonify(response), 202






