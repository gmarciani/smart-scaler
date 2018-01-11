from flask import Blueprint, current_app
from flask import jsonify
from datetime import datetime
import requests


kube = Blueprint("kube", __name__)


@kube.route("/kube/state", methods=["GET"])
def get_kube_state():
    """
    Get the status of Kubernetes cluster.
    :return: (json) the status of Kubernetes cluster.
    """
    kube_state = _get_kube_state()

    response = {
       "ts": datetime.now(),
       "kube_state": kube_state
    }

    return jsonify(response)


def _get_kube_state():
    """
    Get the status of Kubernetes cluster.
    :return: (dict) the Kubernetes status.
    """
    service_host = current_app.config["AGENTS_MANAGER_HOST"]
    service_port = current_app.config["AGENTS_MANAGER_PORT"]

    url_kube_state_service = "http://{}:{}/status".format(service_host, service_port)

    try:
        return requests.get(url_kube_state_service, timeout=5).json()
    except requests.ConnectionError:
        return {"kube_state": "AGENTS MANAGER UNREACHABLE"}