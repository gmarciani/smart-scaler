import requests
from exceptions.repo_exception import RepositoryException


def get(host, port, context, key):
    """
    Get the key value.
    :param host: (string) the repo hostname.
    :param port: (integer) the repo port number.
    :param context: (string) the context id.
    :param key: (string) the key.
    :return: (string) the value.
    """
    url = "http://{}:{}/database".format(host, port)

    full_key = context + "." + key

    data = {
        "key": full_key
    }

    response = requests.get(url, params=data)

    if response.status_code is not 200:
        raise RepositoryException(response.status_code, response.json()["error"])

    return response.json()["value"]


def set(host, port, context, key, value):
    """
    Set the key value.
    :param host: (string) the repo hostname.
    :param port: (integer) the repo port number.
    :param context: (string) the context id.
    :param key: (string) the key.
    :param value: (string) the value.
    :return: (string) the old value.
    """
    url = "http://{}:{}/database".format(host, port)

    full_key = context + "." + key

    data = {
        "key": full_key,
        "value": value
    }

    response = requests.post(url, json=data)

    if response.status_code is not 200:
        raise RepositoryException(response.status_code, response.json()["error"])

    return response.json()["value_old"]


def delete(host, port, context, key):
    """
    Delete the key.
    :param host: (string) the repo hostname.
    :param port: (integer) the repo port number.
    :param context: (string) the context id.
    :param key: (string) the key.
    :return: (string) the old value.
    """
    url = "http://{}:{}/database".format(host, port)

    full_key = context + "." + key

    data = {
        "key": full_key
    }

    response = requests.delete(url, json=data)

    if response.status_code is not 200:
        raise RepositoryException(response.status_code, response.json()["error"])

    return response.json()["value_old"]


