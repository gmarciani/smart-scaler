from flask import Blueprint, current_app
from flask import jsonify, request
from datetime import datetime
from control_repo_manager import repo_simulation as repo_ctrl
from requests.exceptions import ConnectionError
from exceptions.repo_exception import RepositoryException

repo = Blueprint("repo", __name__)


@repo.route("/repo", methods=["GET"])
def repo_get():
    """
    Get the value for a key.
    :return: (json) the response.
    """
    data = request.args

    try:
        context = data["context"]
        key = data["key"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'context', 'key'"
        }
        return jsonify(response), 400

    try:
        value = repo_ctrl.get(current_app.config["REDIS_HOST"], current_app.config["REDIS_PORT"], context, key)
    except ConnectionError as exc:
        response = {
            "ts": datetime.now(),
            "error": "Cannot connect to repository: {}".format(str(exc))
        }
        return jsonify(response), 500
    except RepositoryException as exc:
        response = {
            "ts": datetime.now(),
            "error": "Error from repository: {}".format(exc.message)
        }
        return jsonify(response), exc.code

    response = {
        "ts": datetime.now(),
        "key": key,
        "value": value
    }
    return jsonify(response), 200


@repo.route("/repo", methods=["POST"])
def repo_set():
    """
    Set the value of the key.
    :return: (json) the response.
    """
    data = request.get_json()

    try:
        context = data["context"]
        key = data["key"]
        value_new = data["value"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'context', 'key', 'value'"
        }
        return jsonify(response), 400

    try:
        value_old = repo_ctrl.set(current_app.config["REDIS_HOST"], current_app.config["REDIS_PORT"], context, key, value_new)
    except ConnectionError as exc:
        response = {
            "ts": datetime.now(),
            "error": "Cannot connect to repository: {}".format(str(exc))
        }
        return jsonify(response), 500
    except RepositoryException as exc:
        response = {
            "ts": datetime.now(),
            "error": "Error from repository: {}".format(exc.message)
        }
        return jsonify(response), exc.code

    response = {
        "ts": datetime.now(),
        "key": key,
        "value_new": value_new,
        "value_old": value_old
    }
    return jsonify(response)


@repo.route("/repo", methods=["DELETE"])
def repo_delete():
    """
    Delete the key.
    :return: (json) the response.
    """
    data = request.get_json()

    try:
        context = data["context"]
        key = data["key"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'context', 'key'"
        }
        return jsonify(response), 400

    try:
        value_old = repo_ctrl.delete(current_app.config["REDIS_HOST"], current_app.config["REDIS_PORT"], context, key)
    except ConnectionError as exc:
        response = {
            "ts": datetime.now(),
            "error": "Cannot connect to repository: {}".format(str(exc))
        }
        return jsonify(response), 500
    except RepositoryException as exc:
        response = {
            "ts": datetime.now(),
            "error": "Error from repository: {}".format(exc.message)
        }
        return jsonify(response), exc.code

    response = {
        "ts": datetime.now(),
        "key": key,
        "value_old": value_old
    }
    return jsonify(response)





#@repo.route("/repo", method=["GET"])
#def redis_get(key):
#    """
#    Get the value of the key.
#    :param key: (string) the key.
#    :return: (json) the response.
#    """
#    value = repo_production.get_value(db, key)
#
#    response = {
#        "ts": datetime.now(),
#        "key": key,
#        "value": value
#    }
#
#    return jsonify(response)


#@repo.route("/repo", methods=["POST"])
#def redis_set():
#    """
#    Set the value of the key.
#    :return: (json) the response.
#    """
#    key = request.data["key"]
#    value = request.data["value"]
#
#    new_value = db.set_value(key, value)
#
#    response = {
#        "ts": datetime.now(),
#        "key": key,
#        "value": new_value
#    }
#
#    return jsonify(response)





