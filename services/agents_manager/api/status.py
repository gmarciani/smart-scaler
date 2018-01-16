from flask import Blueprint, current_app
from flask import jsonify
from datetime import datetime
import requests


status = Blueprint("status", __name__)

services = ["kubernetes", "repo_manager"]


@status.route("/status", methods=["GET"])
def get_status():
    """
    Get the status of the service.
    :return: (json) the status of the service.
    """

    statuses = dict([(service, _get_status_service(service)) for service in services])

    response = {
       "ts": datetime.now(),
       "status": "OK" if all(map(lambda x: x["status"] == "OK", statuses.values())) else "FAILED",
       "services": statuses
    }

    return jsonify(response)


def _get_status_service(service_name):
    """
    Get the service status.
    :param service_name: (string) the service name.
    :return: (dict) the service status.
    """
    service_host = current_app.config["{}_HOST".format(service_name.upper())]
    service_port = current_app.config["{}_PORT".format(service_name.upper())]

    url_status_service = "http://{}:{}/status".format(service_host, service_port)

    try:
        return requests.get(url_status_service, timeout=5).json()
    except requests.ConnectionError:
        return {"status": "UNREACHABLE"}
