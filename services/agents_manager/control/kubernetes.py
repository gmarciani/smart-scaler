from common.control import kubernetes as kubernetes_ctrl
from ai.smart_scaling import SmartScaler
from services.common.exceptions.kubernetes_exception import KubernetesException
from services.common.exceptions.repo_manager_exception import RepositoryManagerException
import logging


# Configure logger
logger = logging.getLogger(__name__)


def get_all_smart_scalers(kubernetes_conn):
    """
    Get all Smart Scalers for the specified agents manager.
    :param kubernetes_conn: (SimpleConnection) the Kubernetes connection.
    :return: (list) the list of Smart Scalers for the specified agents manager.
    """
    smart_scalers_all = kubernetes_ctrl.get_all_smart_scalers(kubernetes_conn)
    return smart_scalers_all


def add_local_smart_scaler(smart_scaler, kubernetes_conn, repo_manager_conn, agents):
    """
    Add a Smart Scaler, locally.
    :param smart_scaler_name: (string) the Smart Scaler name.
    :param kubernetes_conn: (SimpleConnection) the Kubernetes connection.
    :param repo_manager_conn: (SimpleConnection) the Kubernetes connection.
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    agent_new = SmartScaler(
        kubernetes_conn,
        repo_manager_conn,
        smart_scaler["name"],
        smart_scaler["pod_name"],
        smart_scaler["min_replicas"] | 1,
        smart_scaler["max_replicas"] | 10
    )

    initialized = agent_new.has_learning_context()

    if initialized:
        logger.debug("Agent {} already have an initialized qlearning context".format(agent_new.name))
    else:
        logger.debug("Agent {} does not have any qlearning context".format(agent_new.name))

    attempts = 0
    max_attempts = 3
    while not initialized and attempts < max_attempts:
        attempts += 1
        logger.debug(
            "Initializing context for Agent {}: attempt {}/{}".format(agent_new.name, attempts, max_attempts))
        try:
            agent_new.create_learning_context()
            logger.debug("Successfully initialized context for Agent {}".format(agent_new.name))
            initialized = True
        except KubernetesException as exc:
            logger.warning("Error from Kubernetes: {}".format(exc.message))
        except RepositoryManagerException as exc:
            logger.warning("Error from Repository Manager: {}".format(exc.message))

    if initialized:
        agents[agent_new.name] = agent_new
        logger.debug("Added Smart Scaler {}".format(agent_new))


def delete_local_smart_scaler(smart_scaler_name, agents):
    """
    Delete a Smart Scaler, locally.
    :param smart_scaler_name: (string) the Smart Scaler name.
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    agent = agents[smart_scaler_name]
    removed = False
    attempts = 0
    max_attempts = 3
    while not removed and attempts < max_attempts:
        attempts += 1
        logger.debug(
            "Removing context for Agent {}: attempt {}/{}".format(agent.name, attempts, max_attempts))
        try:
            agent.remove_learning_context()
            logger.debug("Successfully removed context for Agent {}".format(agent.name))
            removed = True
        except KubernetesException as exc:
            logger.warning("Error from Kubernetes: {}".format(str(exc)))
        except RepositoryManagerException as exc:
            if exc.code == 404:
                removed = True
            logger.warning("Error from Repository Manager: {}".format(exc.message))

    if removed:
        del agents[agent.name]
        logger.debug("Removed Smart Scaler {}".format(agent.name))