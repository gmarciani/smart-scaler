from flask import Blueprint, current_app
from flask import jsonify
from datetime import datetime
from control_api_gateway import kubernetes as kubernetes_ctrl


kubernetes = Blueprint("kubernetes", __name__)


@kubernetes.route("/kubernetes/state", methods=["GET"])
def get_kube_state():
    """
    Get the status of Kubernetes cluster.
    :return: (json) the status of Kubernetes cluster.
    """
    kube_host = current_app.config["KUBERNETES_HOST"]
    kube_port = current_app.config["KUBERNETES_PORT"]

    kube_state = kubernetes_ctrl.get_state(kube_host, kube_port)

    response = {
       "ts": datetime.now(),
       "kube_state": kube_state
    }

    return jsonify(response)


