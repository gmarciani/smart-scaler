from flask import Blueprint, current_app
from flask import jsonify
from datetime import datetime
from api import repo

status = Blueprint("status", __name__)

db = repo.create_connection(current_app.config["REDIS_HOST"], current_app.config["REDIS_PORT"])


@status.route("/status", method=["GET"])
def get_status():
    """
    Get the status of the service.
    :return: (json) the status of the service.
    """
    response = {
        "ts": datetime.now(),
        "status": "OK" if repo.is_available(db) else "REPO UNREACHABLE"
    }

    return jsonify(response)






