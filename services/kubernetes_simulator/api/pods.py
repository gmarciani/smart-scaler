from flask import Blueprint, request, jsonify
from datetime import datetime
from model.registry import PODS_DB, SMART_SCALERS
from model.pod import Pod
from copy import deepcopy


pods = Blueprint("pods", __name__)


@pods.route("/pods", methods=["GET"])
def get_pods():
    """
    Get all Pods or specific Pod.
    :return:
    """
    if not request.args:  # get all pods
        response = {
            "ts": datetime.now(),
            "pods": [vars(pod) for pod in PODS_DB.values()]
        }

    else:  # get specific pod
        pod_name = request.args["name"]
        if pod_name not in PODS_DB:
            return "Pod not found: {}".format(pod_name), 404

        pod = PODS_DB[pod_name]

        response = {
            "ts": datetime.now(),
            "pod": vars(pod)
        }

    return jsonify(response), 200


@pods.route("/pods", methods=["PUT"])
def create_pod():
    """
    Create a new Pod.
    :return:
    """
    data = request.get_json()
    pod_name = data["name"]
    pod_replicas = int(data["replicas"]) if "replicas" in data else 1

    if pod_name in PODS_DB:
        return "Pod already exists: {}".format(pod_name), 400

    pod_new = Pod(pod_name, pod_replicas)
    PODS_DB[pod_name] = pod_new
    response = {
        "ts": datetime.now(),
        "pod_created": vars(pod_new)
    }

    return jsonify(response), 201


@pods.route("/pods/scale", methods=["POST"])
def scale_pod():
    """
    Scale a Pod.
    :return:
    """
    data = request.get_json()

    pod_name = data["name"]
    pod_replicas = int(data["replicas"])

    if pod_name not in PODS_DB:
        return "Pod not found: {}".format(pod_name), 404

    pod_scaled = PODS_DB[pod_name]
    pod_scaled.replicas = pod_replicas

    response = {
        "ts": datetime.now(),
        "pod_scaled": vars(pod_scaled)
    }

    return jsonify(response), 200


@pods.route("/pods", methods=["DELETE"])
def delete_pod():
    """
    Delete a Pod.
    :return:
    """
    data = request.get_json()
    pod_name = data["name"]

    if pod_name not in PODS_DB:
        return "Pod not found: {}".format(pod_name), 404

    pod_deleted = deepcopy(PODS_DB[pod_name])
    del PODS_DB[pod_name]

    smart_scaler_name_to_delete = next((x.name for x in SMART_SCALERS.values() if x.pod_name == pod_name), None)

    smart_scaler_deleted = None
    if smart_scaler_name_to_delete is not None:
        smart_scaler_deleted = deepcopy(SMART_SCALERS[smart_scaler_name_to_delete])
        del SMART_SCALERS[smart_scaler_name_to_delete]

    response = {
        "ts": datetime.now(),
        "pod_deleted": vars(pod_deleted),
        "smart_scaler_deleted": vars(smart_scaler_deleted) if smart_scaler_deleted is not None else None
    }

    return jsonify(response), 202


@pods.route("/pods/status", methods=["GET"])
def get_pod_status():
    """
    Get a Pod status.
    :return:
    """
    pod_name = request.args["name"]
    if pod_name not in PODS_DB:
        return "Pod not found: {}".format(pod_name), 404

    pod = PODS_DB[pod_name]

    response = {
        "ts": datetime.now(),
        "pod_name": pod.name,
        "replicas": pod.replicas,
        "cpu_utilization": pod.cpu_utilization
    }

    return jsonify(response), 200


@pods.route("/pods/status", methods=["POST"])
def set_pod_status():
    """
    Set a Pod status.
    :return:
    """
    data = request.get_json()
    pod_name = data["name"]
    pod_cpu_utilization = data["cpu_utilization"]

    if pod_name not in PODS_DB:
        return "Pod not found: {}".format(pod_name), 404

    pod = PODS_DB[pod_name]
    pod.cpu_utilization = pod_cpu_utilization

    response = {
        "ts": datetime.now(),
        "pod": vars(pod)
    }

    return jsonify(response), 200







