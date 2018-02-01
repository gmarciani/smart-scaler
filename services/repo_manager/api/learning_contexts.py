from flask import Blueprint
from flask import jsonify, request
from datetime import datetime
from services.repo_manager.control import learning_contexts as context_ctrl
from services.common.control import connections as conn_ctrl
from services.common.exceptions.repo_manager_exception import RepositoryManagerException

learning_contexts = Blueprint("learning_contexts", __name__)


@learning_contexts.route("/learning_contexts", methods=["PUT"])
def create_learning_context():
    """
    Create a new qlearning context.
    :return: (json) the response.
    """
    data = request.get_json()

    try:
        context_id = data["context_id"]
        context_params = data["context_params"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'context_id', 'context_params'"
        }
        return jsonify(response), 400

    try:
        repo_conn = conn_ctrl.open_repository_connection()
        context = context_ctrl.create_learning_context(repo_conn, context_id, context_params)
    except RepositoryManagerException as exc:
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
    Delete a qlearning context.
    :return: (json) the response.
    """
    data = request.get_json()

    try:
        context_id = data["context_id"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'context_id'"
        }
        return jsonify(response), 400

    try:
        repo_conn = conn_ctrl.open_repository_connection()
        context_deleted = context_ctrl.delete_learning_context(repo_conn, context_id)
    except RepositoryManagerException as exc:
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
    Get a qlearning context.
    :return: (json) the response.
    """
    data = request.args

    try:
        context_id = data["context_id"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'context_id'"
        }
        return jsonify(response), 400

    try:
        repo_conn = conn_ctrl.open_repository_connection()
        context = context_ctrl.get_learning_context(repo_conn, context_id)
    except RepositoryManagerException as exc:
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
    Check if qlearning context exists.
    :return: (json) the response.
    """
    data = request.args

    try:
        context_id = data["context_id"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'context_id'"
        }
        return jsonify(response), 400

    try:
        repo_conn = conn_ctrl.open_repository_connection()
        context_exists = context_ctrl.exists_learning_context(repo_conn, context_id)
    except RepositoryManagerException as exc:
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


@learning_contexts.route("/learning_contexts", methods=["PATCH"])
def update_learning_context():
    """
    Update an existing qlearning context.
    :return: (json) the response.
    """
    data = request.get_json()

    try:
        context_id = data["context_id"]
        context = data["context"]
    except KeyError:
        response = {
            "ts": datetime.now(),
            "error": "Cannot find field(s) 'context_id', 'context'"
        }
        return jsonify(response), 400

    try:
        repo_conn = conn_ctrl.open_repository_connection()
        context = context_ctrl.update_learning_context(repo_conn, context_id, context)
    except RepositoryManagerException as exc:
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