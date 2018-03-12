from flask import g
from services.common.control import connections as connections_ctrl
from services.common.control import redis_repo as repository_ctrl
from services.common.util import sysutil


# Constants
AUID = "auid"
REPOSITORY = "repository"
KUBERNETES = "kubernetes"


def get_auid():
    """
    Retrieve the Agent Unique ID.
    :return: (str) the Agent Unique ID.
    """
    if not hasattr(g, AUID):
        auid = sysutil.get_puid()
        setattr(g, AUID, auid)
    return getattr(g, AUID)


def get_repository():
    """
    Retrieve an active client to the repository.
    :return: an active client to the repository.
    """
    if not hasattr(g, REPOSITORY):
        repository_conn = connections_ctrl.get_connection("repository")
        setattr(g, REPOSITORY, repository_ctrl.create_connection(repository_conn.host, repository_conn.port))
    return getattr(g, REPOSITORY)


def close_repository():
    """
    Teardown an active client to the repository.
    :return: None
    """
    if hasattr(g, REPOSITORY):
        delattr(g, REPOSITORY)


def get_kubernetes():
    """
    Retrieve an active client to Kubernetes.
    :return: an active client to Kubernetes.
    """
    if not hasattr(g, KUBERNETES):
        setattr(g, KUBERNETES, connections_ctrl.get_connection("kubernetes"))
    return getattr(g, KUBERNETES)


def close_kubernetes():
    """
    Teardown an active client to the repository.
    :return: None
    """
    if hasattr(g, KUBERNETES):
        delattr(g, KUBERNETES)