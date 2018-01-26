from flask import Blueprint
from flask import jsonify
from services.common.control import status as status_ctrl


status = Blueprint("status", __name__)


@status.route("/status", methods=["GET"])
def get_status():
    """
    Get the status of the service.
    :return: (json) the status of the service.
    """
    response = status_ctrl.compose_status_fake()

    return jsonify(response)





