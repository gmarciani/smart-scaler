import requests
from exceptions.repo_exception import RepositoryException


def get_key(host, port, key):
    """
    Get the key value.
    :param host: (string) the repo hostname.
    :param port: (integer) the repo port number.
    :param key: (string) the key.
    :return: the value.
    """
    url = "http://{}:{}/database".format(host, port)

    data = {
        "key": key
    }

    response = requests.get(url, params=data)

    if response.status_code != 200:
        raise RepositoryException(response.status_code, response.json()["error"])

    return response.json()["value"]


def set_key(host, port, key, value, unique=False):
    """
    Set the key value.
    :param host: (string) the repo hostname.
    :param port: (integer) the repo port number.
    :param key: (string) the key.
    :param value: (string) the value.
    :param unique: (bool) if True, raise error if key already exists;if False, overwrite.
    :return: (string) the old value.
    """
    url = "http://{}:{}/database".format(host, port)

    data = {
        "key": key,
        "value": value
    }

    if unique is True:
        response = requests.put(url, json=data)
    else:
        response = requests.post(url, json=data)

    if response.status_code != 200:
        raise RepositoryException(response.status_code, response.json()["error"])

    return response.json()["value_new"]


def delete_key(host, port, key):
    """
    Delete the key.
    :param host: (string) the repo hostname.
    :param port: (integer) the repo port number.
    :param key: (string) the key.
    :return: (string) the old value.
    """
    url = "http://{}:{}/database".format(host, port)

    data = {
        "key": key
    }

    response = requests.delete(url, json=data)

    if response.status_code != 200:
        raise RepositoryException(response.status_code, response.json()["error"])

    return response.json()["value_old"]


def has_key(host, port, key):
    """
    Check if key exists.
    :param host: (string) the repo hostname.
    :param port: (integer) the repo port number.
    :param key: (string) the key.
    :return: (boolean) True, if key exists; False, otherwise.
    """
    try:
        get_key(host, port, key)
    except RepositoryException as exc:
        if exc.code == 404:
            return False
        else:
            raise RepositoryException(exc.code, exc.message)
    return True


