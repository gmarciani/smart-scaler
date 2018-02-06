from flask import Blueprint, current_app
from flask import jsonify
from services.common.control import status as status_ctrl

status = Blueprint("status", __name__)

SERVICES = ["redis"]


@status.route("/status", methods=["GET"])
def get_status():
    """
    Get the status of the service.
    :return: (json) the status of the service.
    """
    statuses = status_ctrl.get_statuses(SERVICES, current_app.config)

    response = status_ctrl.compose_status_respose(statuses)

    return jsonify(response)







