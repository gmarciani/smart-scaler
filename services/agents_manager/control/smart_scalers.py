from services.common.model.exceptions.kubernetes_exception import KubernetesException
from services.common.model.exceptions.repository_exception import RepositoryException
from services.common.control import kubernetes as kubernetes_ctrl
from services.agents_manager.model.smart_scalers_registry import SimpleSmartScalersRegistry as SmartScalersRegistry
from services.common.model.ai.smart_scaling.agent import SmartScaler
import logging


# Configure logger
logger = logging.getLogger(__name__)


SMART_SCALERS_REGISTRY = SmartScalersRegistry()


def get_local_registry():
    """
    Retrieve the local registry of smart scalers.
    :return: the local regisry of smart scalers.
    """
    return SMART_SCALERS_REGISTRY


def update_registry(smart_scalers_local, kubernetes_conn, repository_conn):
    """
    Update the agents registry pulling currently active Smart Scalers on Kubernetes.
    :param smart_scalers_local: (dict) the repository of agents ({smart_scaler_name: agent}).
    :param kubernetes_conn: (SimpleConnection) the connection to Kubernetes.
    :param repository_conn: (SimpleConnection) the connection to the repository.
    :return: None
    """
    smart_scalers_remote = kubernetes_ctrl.get_all_smart_scalers(kubernetes_conn)

    smart_scalers_to_remove = list(set(map(lambda x: x.name, smart_scalers_local)) - set(map(lambda x: x.name, smart_scalers_remote)))

    smart_scalers_to_add = list(filter(lambda x: x.name not in smart_scalers_local, smart_scalers_remote))

    logger.debug("Smart Scaler(s) ALL: {}".format(smart_scalers_remote))
    logger.debug("Smart Scaler(s) to remove: {}".format(smart_scalers_to_remove))
    logger.debug("Smart Scaler(s) to add: {}".format(smart_scalers_to_add))

    for smart_scaler in smart_scalers_to_remove:
        delete_local_smart_scaler(smart_scalers_local, smart_scaler)

    for smart_scaler in smart_scalers_to_add:
        add_local_smart_scaler(smart_scalers_local, smart_scaler, repository_conn)


def apply_scaling(agent, kubernetes_conn):
    """
    Apply scaling actions provided by agents.
    :param agents: the smart scaler agent.
    :param kubernetes_conn: (SimpleConnection) the connection to Kubernetes.
    :return: None
    """
    pod_name = agent.pod_name

    pod = kubernetes_ctrl.get_pod(kubernetes_conn, pod_name)

    curr_state = agent.map_state(pod.replicas, pod.cpu_utilization)

    new_replicas = agent.get_replicas(curr_state)

    kubernetes_ctrl.set_pod_replicas(kubernetes_conn, pod_name, new_replicas)


def load_smart_scaler(smart_scaler, repository_conn):
    """
    Apply scaling actions provided by agents.
    :param smart_scaler: the smart scaler agent.
    :param repository_conn: (SimpleConnection) the connection to the repository.
    :return: None
    """
    pass


def store_smart_scaler(smart_scaler, repository_conn):
    """
    Apply scaling actions provided by agents.
    :param smart_scaler: the smart scaler agent.
    :param repository_conn: (SimpleConnection) the connection to the repository.
    :return: None
    """
    pass


def add_local_smart_scaler(smart_scaler, kubernetes_conn, repository_conn, agents):
    """
    Add a Smart Scaler, locally.
    :param smart_scaler_name: (string) the Smart Scaler name.
    :param kubernetes_conn: (SimpleConnection) the connection to Kubernetes.
    :param repository_conn: (SimpleConnection) the connection to the repository.
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    agent_new = SmartScaler(
        kubernetes_conn,
        repository_conn,
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
        except RepositoryException as exc:
            logger.warning("Error from Repository Manager: {}".format(exc.message))

    if initialized:
        agents[agent_new.name] = agent_new
        logger.debug("Added Smart Scaler {}".format(agent_new))


def delete_local_smart_scaler(agents, smart_scaler_name):
    """
    Delete a Smart Scaler, locally.
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :param smart_scaler_name: (string) the Smart Scaler name.
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
        except RepositoryException as exc:
            if exc.code == 404:
                removed = True
            logger.warning("Error from Repository Manager: {}".format(exc.message))

    if removed:
        del agents[agent.name]
        logger.debug("Removed Smart Scaler {}".format(agent.name))

