from flask import Blueprint, current_app
from flask import jsonify, request
from datetime import datetime
from control_repo_manager import learning_context_ctrl as context_ctrl
from requests.exceptions import ConnectionError
from exceptions.repo_exception import RepositoryException

learning_contexts = Blueprint("learning_contexts", __name__)


@learning_contexts.route("/learning_contexts", methods=["PUT"])
def create_learning_context():
    """
    Create a new learning context.
    :return: (json) the response.
    """
    data = request.get_json()

    try:
        context_id = data["context_id"]
        context_params = data["context_params"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'context', 'params'"
        }
        return jsonify(response), 400

    try:
        context = context_ctrl.create_learning_context(current_app.config["REDIS_HOST"], current_app.config["REDIS_PORT"], context_id, context_params)
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
        "context": context
    }
    return jsonify(response)


@learning_contexts.route("/learning_contexts", methods=["DELETE"])
def delete_learning_context():
    """
    Delete a learning context.
    :return: (json) the response.
    """
    data = request.get_json()

    try:
        context_id = data["context_id"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'context'"
        }
        return jsonify(response), 400

    try:
        context_deleted = context_ctrl.delete_learning_context(current_app.config["REDIS_HOST"], current_app.config["REDIS_PORT"], context_id)
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
        "context": context_deleted
    }
    return jsonify(response)


@learning_contexts.route("/learning_contexts", methods=["GET"])
def get_learning_context():
    """
    Get a learning context.
    :return: (json) the response.
    """
    data = request.args

    try:
        context_id = data["context_id"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'context'"
        }
        return jsonify(response), 400

    try:
        context = context_ctrl.get_learning_context(current_app.config["REDIS_HOST"], current_app.config["REDIS_PORT"], context_id)
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
        "context": context
    }
    return jsonify(response), 200


@learning_contexts.route("/learning_contexts/exists", methods=["GET"])
def exists_learning_context():
    """
    Check if learning context exists.
    :return: (json) the response.
    """
    data = request.args

    try:
        context_id = data["context_id"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'context'"
        }
        return jsonify(response), 400

    try:
        context_exists = context_ctrl.exists_learning_context(current_app.config["REDIS_HOST"],
                                                              current_app.config["REDIS_PORT"], context_id)
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
        "context_id": context_id
    }
    return jsonify(response), 200 if context_exists else 404