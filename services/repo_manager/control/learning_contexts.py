from services.repo_manager.control import repo_simulation as repo_ctrl
from services.common.exceptions.repo_manager_exception import RepositoryManagerException as RepositoryException


def create_learning_context(repo_conn, context_id, context_params):
    """
    Create a new qlearning context.
    :param repo_conn: (SimpleConnection) the repository connection.
    :param context_id: (string) the context id.
    :param context_params: (dict) the qlearning parameters.
    :return: the created context.
    """
    context = {
        "context_id": context_id,
        "context_params": context_params,
        "matrix": [[0.0 for _ in range(3)] for _ in range(context_params["state_granularity"])]
    }

    return repo_ctrl.set_key(repo_conn, context_id, context, unique=True)


def update_learning_context(repo_conn, context_id, context):
    """
    Create a new qlearning context.
    :param repo_conn: (SimpleConnection) the repository connection.
    :param context_id: (string) the context id.
    :param context: (dict) the context parameters.
    :return: the updated context.
    """
    context = {
        "context_id": context_id,
        "context": context
    }

    return repo_ctrl.update_key(repo_conn, context_id, context)


def delete_learning_context(repo_conn, context_id):
    """
    Delete a qlearning context.
    :param repo_conn: (SimpleConnection) the repository connection.
    :param context_id: (string) the context id.
    :return: the deleted context.
    """
    return repo_ctrl.delete_key(repo_conn, context_id)


def get_learning_context(repo_conn, context_id):
    """
    Get a qlearning context.
    :param repo_conn: (SimpleConnection) the repository connection.
    :param context_id: (string) the context id.
    :return: (dict) the created context.
    """
    return repo_ctrl.get_key(repo_conn, context_id)


def exists_learning_context(repo_conn, context_id):
    """
    Check whether there is a context with the given context id.
    :param repo_conn: (SimpleConnection) the repository connection.
    :param context_id: (string) the context id.
    :return: (dict) True, if context exists; False, otherwise.
    """
    return repo_ctrl.has_key(repo_conn, context_id)