from flask import Blueprint
from flask import jsonify, request
from datetime import datetime
from model_redis_simulator.database import REDIS_DB

database = Blueprint("database", __name__)


@database.route("/database", methods=["GET"])
def redis_get():
    """
    Get the value of the key.
    :return: (json) the response.
    """
    data = request.args

    if "key" not in data.keys():  # get all values
        response = {
            "ts": datetime.now(),
            "values": REDIS_DB
        }

    else:  # get the value for the given key
        key = data["key"]

        try:
            value = REDIS_DB[key]
        except KeyError:
            response = {
                "ts": datetime.now(),
                "error": "Cannot find key {}".format(key)
            }
            return jsonify(response), 404

        response = {
            "ts": datetime.now(),
            "key": key,
            "value": value
        }

    return jsonify(response), 200


@database.route("/database", methods=["PUT"])
def redis_set_unique():
    """
    Set the value of the key, that must be unique.
    :return: (json) the response.
    """
    data = request.get_json()

    try:
        key = data["key"]
        value_new = data["value"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'key', 'value'"
        }
        return jsonify(response), 400

    if key in REDIS_DB:
        response = {
            "ts": datetime.now(),
            "error": "Cannot create key {} because it already exists".format(key)
        }
        return jsonify(response), 400

    REDIS_DB[key] = value_new

    response = {
        "ts": datetime.now(),
        "key": key,
        "value_new": value_new
    }
    return jsonify(response), 200


@database.route("/database", methods=["POST"])
def redis_set():
    """
    Set the value of the key.
    :return: (json) the response.
    """
    data = request.get_json()

    try:
        key = data["key"]
        value_new = data["value"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'key', 'value'"
        }
        return jsonify(response), 400

    try:
        value_old = REDIS_DB[key]
    except KeyError:
        value_old = None

    REDIS_DB[key] = value_new

    response = {
        "ts": datetime.now(),
        "key": key,
        "value_new": value_new,
        "value_old": value_old
    }
    return jsonify(response), 200


@database.route("/database", methods=["DELETE"])
def redis_delete():
    """
    Delete the key.
    :return: (json) the response.
    """
    data = request.get_json()

    try:
        key = data["key"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'key'"
        }
        return jsonify(response), 400

    try:
        value = REDIS_DB[key]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find key {}".format(key)
        }
        return jsonify(response), 404

    del REDIS_DB[key]

    response = {
        "ts": datetime.now(),
        "key": key,
        "value_old": value
    }
    return jsonify(response), 200






