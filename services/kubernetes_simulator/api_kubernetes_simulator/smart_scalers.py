from flask import Blueprint, request, jsonify
from datetime import datetime
from model_kubernetes_simulator.registry import PODS_DB, SMART_SCALERS
from model_kubernetes_simulator.smart_scaler import SmartScaler
from copy import deepcopy


smart_scalers = Blueprint("smart_scalers", __name__)


@smart_scalers.route("/smart_scalers", methods=["GET"])
def get_smart_scalers():
    """
    Get all Smart Scalers or specific Smart Scaler.
    :return:
    """
    data = request.args

    if "name" not in data.keys():  # get all smart scalers
        response = {
            "ts": datetime.now(),
            "smart_scalers": [vars(smart_scaler) for smart_scaler in SMART_SCALERS.values()]
        }

    else:  # get specific smart scaler
        smart_scaler_name = request.args["name"]

        try:
            smart_scaler = SMART_SCALERS[smart_scaler_name]
        except KeyError:
            response = {
                "ts": datetime.now(),
                "error": "Cannot find Smart Scaler {}".format(smart_scaler_name)
            }
            return jsonify(response), 404

        response = {
            "ts": datetime.now(),
            "smart_scaler": vars(smart_scaler)
        }

    return jsonify(response), 200


@smart_scalers.route("/smart_scalers", methods=["PUT"])
def create_smart_scaler():
    """
    Create a new Smart Scaler.
    :return:
    """
    data = request.get_json()

    try:
        smart_scaler_name = data["name"]
        pod_name = data["pod_name"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'name', 'pod_name'"
        }
        return jsonify(response), 400

    smart_scaler_min_replicas = int(data["min_replicas"]) if "min_replicas" in data else 1
    smart_scaler_max_replicas = int(data["max_replicas"]) if "max_replicas" in data else float("inf")

    if smart_scaler_name in SMART_SCALERS:
        response = {
            "ts": datetime.now(),
            "error": "Cannot create Smart Scaler {} because it already exists".format(smart_scaler_name)
        }
        return jsonify(response), 400

    if pod_name not in PODS_DB:
        response = {
            "ts": datetime.now(),
            "error": "Cannot create Smart Scaler {} because Pod {} does not exist".format(smart_scaler_name, pod_name)
        }
        return jsonify(response), 400

    if any(smart_scaler.pod_name == pod_name for smart_scaler in SMART_SCALERS.values()):
        response = {
            "ts": datetime.now(),
            "error": "Cannot create Smart Scaler {} because Pod {} has been already associated to another Smart Scaler".format(smart_scaler_name, pod_name)
        }
        return jsonify(response), 400

    smart_scaler_new = SmartScaler(smart_scaler_name, pod_name, smart_scaler_min_replicas, smart_scaler_max_replicas)
    SMART_SCALERS[smart_scaler_name] = smart_scaler_new

    response = {
        "ts": datetime.now(),
        "smart_scaler_created": vars(smart_scaler_new)
    }

    return jsonify(response), 200


@smart_scalers.route("/smart_scalers", methods=["DELETE"])
def delete_smart_scaler():
    """
    Delete a Smart Scaler.
    :return:
    """
    data = request.get_json()

    try:
        smart_scaler_name = data["name"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'name'"
        }
        return jsonify(response), 400

    try:
        smart_scaler_deleted = deepcopy(SMART_SCALERS[smart_scaler_name])
        del SMART_SCALERS[smart_scaler_name]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find Smart Scaler {}".format(smart_scaler_name)
        }
        return jsonify(response), 404

    response = {
        "ts": datetime.now(),
        "smart_scaler_deleted": vars(smart_scaler_deleted)
    }

    return jsonify(response), 200
