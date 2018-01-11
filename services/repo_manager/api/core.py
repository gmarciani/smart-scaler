from flask import Blueprint, current_app
from flask import jsonify, request
from datetime import datetime
from api import repo

core = Blueprint("core", __name__)

db = repo.create_connection(current_app.config["REDIS_HOST"], current_app.config["REDIS_PORT"])


@core.route("/core/get/<key>", method=["GET"])
def redis_get(key):
    """
    Get the value of the key.
    :param key: (string) the key.
    :return: (json) the response.
    """
    value = repo.get_value(db, key)

    response = {
        "ts": datetime.now(),
        "key": key,
        "value": value
    }

    return jsonify(response)


@core.route("/core/set", methods=["POST"])
def redis_set():
    """
    Set the value of the key.
    :return: (json) the response.
    """
    key = request.data["key"]
    value = request.data["value"]

    new_value = db.set_value(key, value)

    response = {
        "ts": datetime.now(),
        "key": key,
        "value": new_value
    }

    return jsonify(response)






