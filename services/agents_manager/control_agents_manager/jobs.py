from control_agents_manager import kubernetes_simulation as kubernetes_ctrl
from datetime import datetime
from model_agents_manager.rl_agent import RLAgent
from exceptions.kubernetes_exception import KubernetesException
from exceptions.repo_manager_exception import RepositoryManagerException
from json.decoder import JSONDecodeError
from requests.exceptions import ConnectionError
import logging


# Configure logger
logger = logging.getLogger(__name__)


def main_loop(kubernetes_conn, repo_manager_conn, agents):
    """
    Update agents and apply scaling actions on Kubernetes.
    :param kubernetes_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param repo_manager_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    logger.info("-" * 25)
    try:
        logger.debug("Agents (before update): {}".format(agents))
        _update_agents(kubernetes_conn, repo_manager_conn, agents)
        logger.info("Agents (after update): {}".format(agents))
        _apply_scaling_actions(agents)
    except ConnectionError as exc:
        logger.warning("Cannot connect: {}".format(str(exc)))
        return
    except JSONDecodeError as exc:
        logger.warning("Malformed response: {}".format(str(exc)))
        return
    except KubernetesException as exc:
        logger.warning("Error from Kubernetes: {}".format(exc.message))
        return
    except RepositoryManagerException as exc:
        logger.warning("Error from Repository Manager: {}".format(exc.message))
        return


def _update_agents(kubernetes_conn, repo_manager_conn, agents):
    """
    Update agents pulling currently active Smart Scalers on Kubernetes.
    :param kubernetes_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param repo_manager_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    smart_scalers_all = _get_all_smart_scalers(kubernetes_conn, repo_manager_conn, 0)

    smart_scalers_to_remove = list(agents.keys() - set(map(lambda x: x["name"], smart_scalers_all)))

    smart_scalers_to_add = list(filter(lambda x: x["name"] not in agents, smart_scalers_all))

    logger.debug("Smart Scaler(s) ALL: {}".format(smart_scalers_all))
    logger.debug("Smart Scaler(s) to remove: {}".format(smart_scalers_to_remove))
    logger.debug("Smart Scaler(s) to add: {}".format(smart_scalers_to_add))

    for smart_scaler_name in smart_scalers_to_remove:
        _delete_smart_scaler(smart_scaler_name, agents)

    for smart_scaler in smart_scalers_to_add:
        _add_smart_scaler(smart_scaler, kubernetes_conn, repo_manager_conn, agents)


def _apply_scaling_actions(agents):
    """
    Apply scaling actions provided by agents.
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    for agent in agents.values():
        agent.apply_scaling_action()


def _get_all_smart_scalers(kubernetes_conn, repo_manager_conn, manager_id):
    """
    Get all Smart Scalers for the specified agents manager.
    :param kubernetes_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param repo_manager_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param manager_id (string): the agents manager id.
    :return: (list) the list of Smart Scalers for the specified agents manager.
    """
    smart_scalers_all = kubernetes_ctrl.get_all_smart_scalers(kubernetes_conn)
    # TODO smart_scalers
    # smart_scalers = repo_manager_ctrl.get_all_smart_scalers(repo_manager_conn, manager_id)
    return smart_scalers_all


def _delete_smart_scaler(smart_scaler_name, agents):
    """
    Delete a Smart Scaler.
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
        except ConnectionError as exc:
            logger.warning("Cannot connect to Repository Manager: {}".format(str(exc)))
        except JSONDecodeError as exc:
            logger.warning("Malformed response from Repository Manager: {}".format(str(exc)))
        except RepositoryManagerException as exc:
            if exc.code == 404:
                removed = True
            logger.warning("Error from Repository Manager: {}".format(exc.message))

    if removed:
        del agents[agent.name]
        logger.debug("Removed Smart Scaler {}".format(agent.name))


def _add_smart_scaler(smart_scaler, kubernetes_conn, repo_manager_conn, agents):
    """
    Add a Smart Scaler.
    :param smart_scaler_name: (string) the Smart Scaler name.
    :param kubernetes_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param repo_manager_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    agent_new = RLAgent(
        kubernetes_conn,
        repo_manager_conn,
        smart_scaler["name"],
        smart_scaler["pod_name"],
        smart_scaler["min_replicas"] | 1,
        smart_scaler["max_replicas"] | 10
    )

    initialized = agent_new.has_learning_context()

    if initialized:
        logger.debug("Agent {} already have an initialized learning context".format(agent_new.name))
    else:
        logger.debug("Agent {} does not have any learning context".format(agent_new.name))

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
        except ConnectionError as exc:
            logger.warning("Cannot connect to Repository Manager: {}".format(str(exc)))
        except JSONDecodeError as exc:
            logger.warning("Malformed response from Repository Manager: {}".format(str(exc)))
        except RepositoryManagerException as exc:
            logger.warning("Error from Repository Manager: {}".format(exc.message))

    if initialized:
        agents[agent_new.name] = agent_new
        logger.debug("Added Smart Scaler {}".format(agent_new))


def shutdown_hook(param):
    """
    Perform all shutdown actions.
    :param param: (dict) dictionary of parameters.
    :return: (void)
    """
    logger.info("Shutdown Hook at {}: {}".format(datetime.now(), param))