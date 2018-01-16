from flask import Blueprint, request, jsonify
from datetime import datetime
from model.registry import PODS_DB, SMART_SCALERS
from model.smart_scaler import SmartScaler
from copy import deepcopy


smart_scalers = Blueprint("smart_scalers", __name__)


@smart_scalers.route("/smart_scalers", methods=["GET"])
def get_smart_scalers():
    """
    Get all Smart Scalers or specific Smart Scaler.
    :return:
    """
    if not request.args:  # get all smart scalers
        response = {
            "ts": datetime.now(),
            "smart_scalers": [vars(smart_scaler) for smart_scaler in SMART_SCALERS.values()]
        }

    else:  # get specific smart scaler
        smart_scaler_name = request.args["name"]
        if smart_scaler_name not in SMART_SCALERS:
            return "Smart Scaler not found: {}".format(smart_scaler_name), 404

        smart_scaler = SMART_SCALERS[smart_scaler_name]

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
    smart_scaler_name = data["name"]
    pod_name = data["pod_name"]
    smart_scaler_min_replicas = int(data["min_replicas"]) if "min_replicas" in data else 1
    smart_scaler_max_replicas = int(data["max_replicas"]) if "max_replicas" in data else float("inf")

    if smart_scaler_name in SMART_SCALERS:
        return "Smart Scaler already exists: {}".format(smart_scaler_name), 400

    if any(smart_scaler == pod_name for smart_scaler in SMART_SCALERS):
        return "Smart Scaler already associated to Pod {}: {}".format(pod_name, smart_scaler_name), 400

    if pod_name not in PODS_DB:
        return "Pod does not exist: {}".format(pod_name), 400

    smart_scaler_new = SmartScaler(smart_scaler_name, pod_name, smart_scaler_min_replicas, smart_scaler_max_replicas)
    SMART_SCALERS[smart_scaler_name] = smart_scaler_new
    response = {
        "ts": datetime.now(),
        "smart_scaler_created": vars(smart_scaler_new)
    }

    return jsonify(response), 201


@smart_scalers.route("/smart_scalers", methods=["DELETE"])
def delete_smart_scaler():
    """
    Delete a Smart Scaler.
    :return:
    """
    data = request.get_json()
    smart_scaler_name = data["name"]

    if smart_scaler_name not in SMART_SCALERS:
        return "Smart Scaler not found: {}".format(smart_scaler_name), 404

    smart_scaler_deleted = deepcopy(SMART_SCALERS[smart_scaler_name])
    del SMART_SCALERS[smart_scaler_name]

    response = {
        "ts": datetime.now(),
        "smart_scaler_deleted": vars(smart_scaler_deleted)
    }

    return jsonify(response), 202
