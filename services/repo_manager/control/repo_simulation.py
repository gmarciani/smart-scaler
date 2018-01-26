import requests
import json
from services.common.control import connections as conn_ctrl
from services.common.exceptions.repo_manager_exception import RepositoryManagerException as RepositoryException


def get_key(repo_conn, key):
    """
    Get the key value.
    :param repo_conn: (SimpleConnection) the repository connection.
    :param key: (string) the key.
    :return: the value.
    """
    url = conn_ctrl.format_url("database", repo_conn)

    data = {
        "key": key
    }

    try:
        response = requests.get(url, params=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise RepositoryException(500, str(exc))

    if response.status_code != 200:
        raise RepositoryException(response.status_code, response_json["error"])

    return response_json["value"]


def set_key(repo_conn, key, value, unique=False):
    """
    Set the key value.
    :param repo_conn: (SimpleConnection) the repository connection.
    :param key: (string) the key.
    :param value: (string) the value.
    :param unique: (bool) if True, raise error if key already exists;if False, overwrite.
    :return: (string) the old value.
    """
    url = conn_ctrl.format_url("database", repo_conn)


    data = {
        "key": key,
        "value": value
    }

    try:
        if unique is True:
            response = requests.put(url, json=data)
        else:
            response = requests.post(url, json=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise RepositoryException(500, str(exc))

    if response.status_code != 200:
        raise RepositoryException(response.status_code, response_json["error"])

    return response_json["value_new"]


def update_key(repo_conn, key, value):
    """
    Update the value of an existent key.
    :param repo_conn: (SimpleConnection) the repository connection.
    :param key: (string) the key.
    :param value: (string) the value.
    :return: (string) the old value.
    """
    url = conn_ctrl.format_url("database", repo_conn)

    data = {
        "key": key,
        "value": value
    }

    try:
        response = requests.patch(url, json=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise RepositoryException(500, str(exc))

    if response.status_code != 200:
        raise RepositoryException(response.status_code, response_json["error"])

    return response_json["value_new"]


def delete_key(repo_conn, key):
    """
    Delete the key.
    :param repo_conn: (SimpleConnection) the repository connection.
    :param key: (string) the key.
    :return: (string) the old value.
    """
    url = conn_ctrl.format_url("database", repo_conn)

    data = {
        "key": key
    }

    try:
        response = requests.delete(url, json=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise RepositoryException(500, str(exc))

    if response.status_code != 200:
        raise RepositoryException(response.status_code, response_json["error"])

    return response_json["value_old"]


def has_key(repo_conn, key):
    """
    Check if key exists.
    :param repo_conn: (SimpleConnection) the repository connection.
    :param key: (string) the key.
    :return: (boolean) True, if key exists; False, otherwise.
    """
    try:
        get_key(repo_conn, key)
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise RepositoryException(500, str(exc))
    except RepositoryException as exc:
        if exc.code == 404:
            return False
        else:
            raise RepositoryException(exc.code, exc.message)
    return True


