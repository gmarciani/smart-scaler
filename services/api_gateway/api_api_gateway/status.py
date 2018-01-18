from flask import Blueprint, current_app
from flask import jsonify
from datetime import datetime
from control_api_gateway import status as status_ctrl


status = Blueprint("status", __name__)

SERVICES = ["agents_manager", "repo_manager"]


@status.route("/status", methods=["GET"])
def get_status():
    """
    Get the status of the overall application.
    :return: (json) the status of the overall application.
    """
    statuses = dict([(service, status_ctrl.get_status_service(
        current_app.config["{}_HOST".format(service.upper())],
        current_app.config["{}_PORT".format(service.upper())]))
                     for service in SERVICES])

    response = {
       "ts": datetime.now(),
       "status": "OK" if all(map(lambda x: x["status"] == "OK", statuses.values())) else "FAILED",
       "services": statuses
    }

    return jsonify(response)