from flask import Blueprint
from flask import jsonify, request
from datetime import datetime
from services.repo_manager.control import repo_simulation as repo_ctrl
from services.common.control import connections as conn_ctrl
from services.common.exceptions.repo_manager_exception import RepositoryManagerException

repo = Blueprint("repo", __name__)


@repo.route("/repo", methods=["GET"])
def get_key():
    """
    Get the value for a key.
    :return: (json) the response.
    """
    data = request.args

    try:
        key = data["key"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'key'"
        }
        return jsonify(response), 400

    try:
        repo_conn = conn_ctrl.open_repository_connection()
        value = repo_ctrl.get_key(repo_conn, key)
    except RepositoryManagerException as exc:
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
def set_key():
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
        repo_conn = conn_ctrl.open_repository_connection()
        value_old = repo_ctrl.set_key(repo_conn, key, value_new)
    except RepositoryManagerException as exc:
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
def delete_key():
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
        repo_conn = conn_ctrl.open_repository_connection()
        value_old = repo_ctrl.delete_key(repo_conn, key)
    except RepositoryManagerException as exc:
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


@repo.route("/repo/check", methods=["GET"])
def has_key():
    """
    Check if key exists.
    :return: (json) the response.
    """
    data = request.args

    try:
        key = data["key"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'key'"
        }
        return jsonify(response), 400

    try:
        repo_conn = conn_ctrl.open_repository_connection()
        key_exists = repo_ctrl.has_key(repo_conn, key)
    except RepositoryManagerException as exc:
        response = {
            "ts": datetime.now(),
            "error": "Error from repository: {}".format(exc.message)
        }
        return jsonify(response), exc.code

    response = {
        "ts": datetime.now(),
        "key": key
    }
    return jsonify(response), 200 if key_exists else 404


