import requests
import json
from services.common.control import connections as conn_ctrl
from common.model import RepositoryException


def create_learning_context(repo_manager_conn, context_id, context_params):
    """
    Initialize the qlearning context for the specified context.
    :param repo_manager_conn: (SimpleConnection) the Repository Manager connection.
    :param context_id: (string) the context id.
    :param context_params: (dict) the context parameters.
    :return: (void).
    """
    url = conn_ctrl.format_url("learning_contexts", repo_manager_conn)

    data = {
        "context_id": context_id,
        "context_params": context_params
    }

    try:
        response = requests.put(url, json=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise RepositoryException(500, "create_learning_context: " + str(exc))

    if response.status_code is not 200:
        raise RepositoryException(response.status_code, response_json["error"])


def remove_learning_context(repo_manager_conn, context_id):
    """
    Remove the qlearning context for the specified context.
    :param repo_manager_conn: (SimpleConnection) the Repository Manager connection.
    :param context_id: (string) the context id.
    :return: (void).
    """
    url = conn_ctrl.format_url("learning_contexts", repo_manager_conn)

    data = {
        "context_id": context_id
    }

    try:
        response = requests.delete(url, json=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise RepositoryException(500, "remove_learning_context: " + str(exc))

    if response.status_code is not 200:
        raise RepositoryException(response.status_code, response_json["error"])


def get_learning_context(repo_manager_conn, context_id):
    """
    Get the qlearning context for the specified context.
    :param repo_manager_conn: (SimpleConnection) the Repository Manager connection.
    :param context_id: (string) the context id.
    :return: (dict) the qlearning context.
    """
    url = conn_ctrl.format_url("learning_contexts", repo_manager_conn)

    data = {
        "context_id": context_id
    }

    try:
        response = requests.get(url, params=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise RepositoryException(500, "get_learning_context: " + str(exc))

    if response.status_code is not 200:
        raise RepositoryException(response.status_code, response_json["error"])

    return response_json["context"]


def exists_learning_context(repo_manager_conn, context_id):
    """

    :param repo_manager_conn: (SimpleConnection) the Repository Manager connection.
    :param context_id:
    :return:
    """
    url = conn_ctrl.format_url("learning_contexts/exists", repo_manager_conn)

    data = {
        "context_id": context_id
    }

    try:
        response = requests.get(url, params=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise RepositoryException(500, "exists_learning_context: " + str(exc))

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise RepositoryException(response.status_code, response_json["error"])


def update_learning_context(repo_manager_conn, context_id, context):
    """

    :param repo_manager_conn: (SimpleConnection) the Repository Manager connection.
    :param context_id:
    :param context:
    :return:
    """
    url = conn_ctrl.format_url("learning_contexts", repo_manager_conn)

    data = {
        "context_id": context_id,
        "context": context
    }

    try:
        response = requests.patch(url, json=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise RepositoryException(500, "update_learning_context: " + str(exc))

    if response.status_code is not 200:
        raise RepositoryException(response.status_code, response_json["error"])