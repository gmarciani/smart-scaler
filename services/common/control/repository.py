from services.common.control import connections as conn_ctrl
from services.common.model.exceptions.repository_exception import RepositoryException
import requests
import json
import logging


logger = logging.getLogger(__name__)


def get_key(repository_conn, key):
    """
    Return the value for the key.
    :param repository_conn: (SimpleConnection) the connection to the repository.
    :param key: (string) the key to retrieve the value of.
    :return: (string) the value for the key, if it exists; None, otherwise.
    """
    url = conn_ctrl.format_url("database", repository_conn)

    data = dict(key=key)

    try:
        response = requests.get(url, params=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise RepositoryException(500, "get_key: " + str(exc))

    if response.status_code is 404:
        return None
    elif response.status_code is not 200:
        raise RepositoryException(response.status_code, response_json["error"])

    return response_json["value"]


def set_key(repository_conn, key, value, unique=False):
    """
    Set the value for the key.
    :param repository_conn: (SimpleConnection) the connection to the repository.
    :param key: (string) the key.
    :param value: (string) the value.
    :param value: (string) the value.
    :param unique: (bool) if True, raises an error if key already exists.
    :return: (string) the old value for the key.
    """
    url = conn_ctrl.format_url("database", repository_conn)

    data=dict(key=key, value=value, unique=unique)

    try:
        response = requests.post(url, json=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise RepositoryException(500, "set_key: " + str(exc))

    if response.status_code is 404:
        return None
    elif response.status_code is not 200:
        raise RepositoryException(response.status_code, response_json["error"])

    return response_json["value"]


def delete_key(repository_conn, key):
    """
    Delete the key.
    :param repository_conn: (SimpleConnection) the connection to the repository.
    :param key: (string) the key.
    :return: (string) the value for the key.
    """
    url = conn_ctrl.format_url("database", repository_conn)

    data=dict(key=key)

    try:
        response = requests.delete(url, json=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise RepositoryException(500, "delete_key: " + str(exc))

    if response.status_code is not 200:
        raise RepositoryException(response.status_code, response_json["error"])

    return response_json["value"]