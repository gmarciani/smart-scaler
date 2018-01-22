import requests
from exceptions.repo_manager_exception import RepositoryManagerException


def create_learning_context(repo_manager_conn, context_id, context_params):
    """
    Initialize the learning context for the specified context.
    :param repo_manager_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param context_id: (string) the context id.
    :param context_params: (dict) the context parameters.
    :return: (void).
    """
    host = repo_manager_conn[0]
    port = repo_manager_conn[1]

    url = "http://{}:{}/learning_contexts".format(host, port)

    data = {
        "context_id": context_id,
        "context_params": context_params
    }

    response = requests.put(url, json=data)

    if response.status_code is not 200:
        raise RepositoryManagerException(response.status_code, response.json()["error"])


def remove_learning_context(repo_manager_conn, context_id):
    """
    Remove the learning context for the specified context.
    :param repo_manager_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param context_id: (string) the context id.
    :return: (void).
    """
    host = repo_manager_conn[0]
    port = repo_manager_conn[1]

    url = "http://{}:{}/learning_contexts".format(host, port)

    data = {
        "context_id": context_id
    }

    response = requests.delete(url, json=data)

    if response.status_code is not 200:
        raise RepositoryManagerException(response.status_code, response.json()["error"])


def get_learning_context(repo_manager_conn, context_id):
    """
    Get the learning context for the specified context.
    :param repo_manager_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param context_id: (string) the context id.
    :return: (dict) the learning context.
    """
    host = repo_manager_conn[0]
    port = repo_manager_conn[1]

    url = "http://{}:{}/learning_contexts".format(host, port)

    data = {
        "context_id": context_id
    }

    response = requests.get(url, params=data)

    if response.status_code is not 200:
        raise RepositoryManagerException(response.status_code, response.json()["error"])

    response_json = response.json()

    return response_json["context"]


def exists_learning_context(repo_manager_conn, context_id):
    host = repo_manager_conn[0]
    port = repo_manager_conn[1]

    url = "http://{}:{}/learning_contexts/exists".format(host, port)

    data = {
        "context_id": context_id
    }

    response = requests.get(url, params=data)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise RepositoryManagerException(response.status_code, response.json()["error"])


def update_learning_context(repo_manager_conn, context_id, context):
    host = repo_manager_conn[0]
    port = repo_manager_conn[1]

    url = "http://{}:{}/learning_contexts".format(host, port)

    data = {
        "context_id": context_id,
        "context": context
    }

    response = requests.patch(url, params=data)

    if response.status_code is not 200:
        raise RepositoryManagerException(response.status_code, response.json()["error"])


def get_all_smart_scalers(repo_manager_conn, manager_id):
    # TODO
    pass