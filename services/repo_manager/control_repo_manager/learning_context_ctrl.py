from control_repo_manager import repo_simulation as repo_ctrl
from exceptions.repo_exception import RepositoryException


def create_learning_context(host, port, context_id, context_params):
    """
    Create a new learning context.
    :param host: (string) the repo hostname.
    :param port: (integer) the repo port number.
    :param context_id: (string) the context id.
    :param context_params: (dict) the learning parameters.
    :return: the created context.
    """
    context = {
        "context_id": context_id,
        "context_params": context_params,
        "matrix": [[0.0 for i in range(3)] for j in range(context_params["state_granularity"])]
    }

    return repo_ctrl.set_key(host, port, context_id, context, unique=True)


def update_learning_context(host, port, context_id, context):
    """
    Create a new learning context.
    :param host: (string) the repo hostname.
    :param port: (integer) the repo port number.
    :param context_id: (string) the context id.
    :param context: (dict) the context parameters.
    :return: the updated context.
    """
    context = {
        "context_id": context_id,
        "context": context
    }

    return repo_ctrl.set_key(host, port, context_id, context)


def delete_learning_context(host, port, context_id):
    """
    Delete a learning context.
    :param host: (string) the repo hostname.
    :param port: (integer) the repo port number.
    :param context_id: (string) the context id.
    :return: the deleted context.
    """
    return repo_ctrl.delete_key(host, port, context_id)


def get_learning_context(host, port, context_id):
    """
    Get a learning context.
    :param host: (string) the repo hostname.
    :param port: (integer) the repo port number.
    :param context_id: (string) the context id.
    :return: (dict) the created context.
    """
    return repo_ctrl.get_key(host, port, context_id)


def exists_learning_context(host, port, context_id):
    """
    Check whether there is a context with the given context id.
    :param host: (string) the repo hostname.
    :param port: (integer) the repo port number.
    :param context_id: (string) the context id.
    :return: (dict) True, if context exists; False, otherwise.
    """
    try:
        get_learning_context(host, port, context_id)
    except RepositoryException as exc:
        if exc.code == 404:
            return False
        else:
            raise RepositoryException(exc.code, exc.message)
    return True