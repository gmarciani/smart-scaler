"""
The control layer for Agents Manager Registry management.
"""


from services.common.model.exceptions.service_exception import RepositoryException
from services.common.control import kubernetes as kubernetes_ctrl
from services.common.control import repository as repository_ctrl
from services.agents_manager.model.registry import SimpleAgentsManagerRegistry as SmartScalersRegistry
import logging


# Logging
logger = logging.getLogger(__name__)


# Constants
SMART_SCALERS_REGISTRY = SmartScalersRegistry()


def get_local_registry():
    """
    Retrieve the local Agents Manager Registry.

    :return: the local Agents Manager Registry.
    """
    return SMART_SCALERS_REGISTRY


def update_registry(registry, kubernetes_conn):
    """
    Update the local Agents Manager Registry, pulling Smart Scalers resources from Kubernetes.

    :param registry: (SimpleSmartScalersRegistry) the local registry.
    :param kubernetes_conn: (SimpleConnection) the connection to Kubernetes.
    :return: None
    """
    smart_scaler_resources_remote = kubernetes_ctrl.get_all_smart_scalers(kubernetes_conn)

    smart_scaler_names_to_remove = list(
        set(registry.names()) -
        set(map(lambda smart_scaler_resource: smart_scaler_resource.name, smart_scaler_resources_remote))
    )

    smart_scaler_resources_to_add = list(
        filter(lambda smart_scaler: smart_scaler.resource.name not in registry.names(), smart_scaler_resources_remote)
    )

    logger.debug("Smart Scaler(s) REMOTE (resources): {}".format(smart_scaler_resources_remote))
    logger.debug("Smart Scaler(s) TO REMOVE LOCALLY (names): {}".format(smart_scaler_names_to_remove))
    logger.debug("Smart Scaler(s) TO ADD LOCALLY (resources): {}".format(smart_scaler_resources_to_add))

    for name in smart_scaler_names_to_remove:
        delete_smart_scaler(registry, name)

    for resource in smart_scaler_resources_to_add:
        add_smart_scaler(registry, resource)


def add_smart_scaler(smart_scalers_local, smart_scaler_resource, repository_conn, max_attempts=3):
    """
    Add a smart scaler resource.
    :param smart_scalers_local: (SimpleSmartScalersRegistry) the local repository of smart scalers.
    :param smart_scaler_resource: (SmartScalerResource) the smart scaler resource.
    :param repository_conn: (SimpleConnection) the connection to the repository.
    :param max_attempts: (int) the maximum number of attempts.
    :return: None
    """
    initialized = repository_ctrl.get_key(repository_conn, smart_scaler_resource.name) is not None

    if initialized:
        logger.debug("Smart scaler {} is already present in remote repository".format(smart_scaler_resource.name))
    else:
        logger.debug("Smart scaler {} is not yet present in remote repository".format(smart_scaler_resource.name))

    attempts = 0
    while not initialized and attempts < max_attempts:
        attempts += 1
        logger.debug(
            "Adding smart scaler {} to remote repository: attempt {}/{}".format(smart_scaler_resource.name, attempts, max_attempts))
        try:
            repository_ctrl.set_key(repository_conn, smart_scaler_resource.name, smart_scaler_resource.to_binarys(), unique=True)
            logger.debug("Added smart scaler {} to remote repository".format(smart_scaler_resource.name))
            initialized = True
        except RepositoryException as exc:
            logger.warning("Error from Repository: {}".format(exc.message))

    if initialized:
        smart_scalers_local[smart_scaler_resource.name] = smart_scaler_resource
        logger.debug("Added smart scaler {}".format(smart_scaler_resource))


def delete_smart_scaler(smart_scalers_local, smart_scaler_name, repository_conn, max_attempts=3):
    """
    Delete a smart scaler.
    :param smart_scalers_local: (dict) the repository of agents ({smart_scaler_name: agent}).
    :param smart_scaler_name: (string) the Smart Scaler name.
    :param repository_conn: (SimpleConnection) the connection to the repository.
    :param max_attempts: (int) maximum number of connection attempts.
    :return: None
    """
    removed = False
    attempts = 0
    while not removed and attempts < max_attempts:
        attempts += 1
        logger.debug(
            "Removing smart scaler {} from repository: attempt {}/{}".format(smart_scaler_name, attempts, max_attempts))
        try:
            repository_ctrl.delete_key(repository_conn, smart_scaler_name)
            removed = True
        except RepositoryException as exc:
            logger.warning("Error from Repository: {}".format(exc.message))
            if exc.code == 404:
                removed = True
    if removed:
        logger.debug("Removed smart scaler {} from remote repository".format(smart_scaler_name))
        del smart_scalers_local[smart_scaler_name]
        logger.debug("Removed smart scaler {} from local registry".format(smart_scaler_name))
    else:
        logger.error("Cannot remove smart scaler {} from remote repository".format(smart_scaler_name))
