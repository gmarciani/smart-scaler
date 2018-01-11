from flask import Blueprint, current_app
from flask import jsonify
from datetime import datetime


status = Blueprint("status", __name__)


@status.route("/status", methods=["GET"])
def get_status():
    """
    Get the status of the service.
    :return: (json) the status of the service.
    """

    response = {
        "ts": datetime.now(),
        "status": "OK"
    }

    return jsonify(response)
