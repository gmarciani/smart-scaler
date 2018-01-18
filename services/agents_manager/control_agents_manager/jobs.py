from control_agents_manager import kubernetes_simulation as kubernetes_ctrl
from datetime import datetime
from model_agents_manager.rl_agent import RLAgent
from exceptions.kubernetes_exception import KubernetesException
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
    _update_agents(kubernetes_conn, repo_manager_conn, agents)
    logger.info("Agents: {}".format(agents))
    _apply_scaling_actions(agents)


def _update_agents(kubernetes_conn, repo_manager_conn, agents):
    """
    Update agents pulling currently active Smart Scalers on Kubernetes.
    :param kubernetes_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param repo_manager_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    try:
        smart_scalers = kubernetes_ctrl.get_all_kube_smart_scalers(kubernetes_conn)
    except ConnectionError as exc:
        logger.warning("Cannot connect to Kubernetes: {}".format(str(exc)))
        return
    except JSONDecodeError as exc:
        logger.warning("Malformed response from Kubernetes: {}".format(str(exc)))
        return
    except KubernetesException as exc:
        logger.warning("Error from Kubernetes: {}".format(exc.message))
        return

    smart_scalers_to_remove = list(agents.keys() - set(map(lambda x: x["name"], smart_scalers)))

    smart_scalers_to_add = list(filter(lambda x: x["name"] not in agents, smart_scalers))

    for smart_scaler_name in smart_scalers_to_remove:
        del agents[smart_scaler_name]
        logger.debug("Removed Smart Scaler: {}".format(smart_scaler_name))

    for smart_scaler in smart_scalers_to_add:
        agent_new = RLAgent(
            kubernetes_conn,
            repo_manager_conn,
            smart_scaler["name"],
            smart_scaler["pod_name"],
            smart_scaler["min_replicas"] | 1,
            smart_scaler["max_replicas"] | 10
        )
        agents[smart_scaler["name"]] = agent_new
        logger.debug("Added Smart Scaler: {}".format(agent_new))


def _apply_scaling_actions(agents):
    """
    Apply scaling actions provided by agents.
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    for agent in agents.values():
        agent.apply_scaling_action()


def shutdown_hook(param):
    """
    Perform all shutdown actions.
    :param param: (dict) dictionary of parameters.
    :return: (void)
    """
    logger.info("Shutdown Hook at {}: {}".format(datetime.now(), param))