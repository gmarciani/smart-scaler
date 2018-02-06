from flask import Blueprint, request, jsonify
from datetime import datetime
from services.kubernetes_simulator.model.registry import PODS_DB, SMART_SCALERS
from common.model.pod import Pod
from copy import deepcopy


pods = Blueprint("pods", __name__)


@pods.route("/pods", methods=["GET"])
def get_pods():
    """
    Get all Pods or specific Pod.
    :return:
    """
    data = request.args

    if "name" not in data.keys():  # get all pods
        response = {
            "ts": datetime.now(),
            "pods": [vars(pod) for pod in PODS_DB.values()]
        }

    else:  # get specific pod
        pod_name = data["name"]

        try:
            pod = PODS_DB[pod_name]
        except KeyError:
            response = {
                "ts": datetime.now(),
                "error": "Cannot find Pod {}".format(pod_name)
            }
            return jsonify(response), 404

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

    try:
        pod_name = data["name"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'name'"
        }
        return jsonify(response), 400

    pod_replicas = int(data["replicas"]) if "replicas" in data else 1

    if pod_name in PODS_DB:
        response = {
            "ts": datetime.now(),
            "error": "Cannot create Pod {} because it already exists".format(pod_name)
        }
        return jsonify(response), 400

    pod_new = Pod(pod_name, pod_replicas)
    PODS_DB[pod_name] = pod_new

    response = {
        "ts": datetime.now(),
        "pod_created": vars(pod_new)
    }

    return jsonify(response), 200


@pods.route("/pods", methods=["DELETE"])
def delete_pod():
    """
    Delete a Pod.
    :return:
    """
    data = request.get_json()

    try:
        pod_name = data["name"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'name'"
        }
        return jsonify(response), 400

    try:
        pod_deleted = deepcopy(PODS_DB[pod_name])
        del PODS_DB[pod_name]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find Pod {}".format(pod_name)
        }
        return jsonify(response), 404

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

    return jsonify(response), 200


@pods.route("/pods/scale", methods=["POST"])
def scale_pod():
    """
    Scale a Pod.
    :return:
    """
    data = request.get_json()

    try:
        pod_name = data["name"]
        pod_replicas = int(data["replicas"])
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'name', 'replicas'"
        }
        return jsonify(response), 400

    try:
        pod_scaled = PODS_DB[pod_name]
        replicas_old = pod_scaled.replicas
        pod_scaled.replicas = pod_replicas
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find Pod {}".format(pod_name)
        }
        return jsonify(response), 404

    response = {
        "ts": datetime.now(),
        "pod_scaled": vars(pod_scaled),
        "replicas_old": replicas_old
    }

    return jsonify(response), 200


@pods.route("/pods/status", methods=["GET"])
def get_pod_status():
    """
    Get a Pod status.
    :return:
    """
    data = request.args

    try:
        pod_name = data["name"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'name'"
        }
        return jsonify(response), 400

    try:
        pod = PODS_DB[pod_name]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find Pod {}".format(pod_name)
        }
        return jsonify(response), 404

    response = {
        "ts": datetime.now(),
        "pod_name": pod.name,
        "status": {
            "replicas": pod.replicas,
            "cpu_utilization": pod.cpu_utilization
        }
    }

    return jsonify(response), 200


@pods.route("/pods/status", methods=["POST"])
def set_pod_status():
    """
    Set a Pod status.
    :return:
    """
    data = request.get_json()

    try:
        pod_name = data["name"]
        pod_cpu_utilization = data["cpu_utilization"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'name'"
        }
        return jsonify(response), 400

    try:
        pod = PODS_DB[pod_name]
        pod.cpu_utilization = pod_cpu_utilization
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find Pod {}".format(pod_name)
        }
        return jsonify(response), 404

    response = {
        "ts": datetime.now(),
        "pod": vars(pod)
    }

    return jsonify(response), 200







