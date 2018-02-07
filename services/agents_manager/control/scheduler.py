from flask import g, current_app
from services.common.control import connections as connections_ctrl
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from services.agents_manager.control import agents_registry as agents_registry_ctrl
from services.agents_manager.control import kubernetes as smart_scalers_ctrl
from services.common.exceptions.kubernetes_exception import KubernetesException
from services.common.exceptions.repo_manager_exception import RepositoryManagerException


def get_scheduler():
    """
    Retrieve the scheduler.
    :return: (dict) the scheduler.
    """
    scheduler = getattr(g, "_scheduler", None)
    if scheduler is None:
        scheduler = g._scheduler = __init_scheduler()
    return scheduler


def teardown_scheduler():
    """
    Teardown the scheduler.
    :return: (void)
    """
    scheduler = getattr(g, "_scheduler", None)
    if scheduler is not None:
        scheduler.shutdown()


def __init_scheduler():
    """
    Create a new scheduler.
    :return: the scheduler.
    """
    config = current_app.config

    kubernetes_conn = connections_ctrl.get_service_connection("kubernetes", config)
    repository_conn = connections_ctrl.get_service_connection("repository", config)
    kubernetes_pull = config["KUBERNETES_PULL"]
    agents = agents_registry_ctrl.get_registry()

    scheduler = BackgroundScheduler()
    scheduler.add_job(id="main_loop", func=main_loop,
                      kwargs={
                          "kubernetes_conn": kubernetes_conn,
                          "repository_conn": repository_conn,
                          "agents": agents
                      },
                      trigger=IntervalTrigger(seconds=kubernetes_pull),
                      max_instances=1,
                      coalesce=True)


def main_loop(kubernetes_conn, repo_manager_conn, agents):
    """
    Update agents and apply scaling actions on Kubernetes.
    :param kubernetes_conn: (SimpleConnection) the Kubernetes connection.
    :param repo_manager_conn: (SimpleConnection) the Kubernetes connection.
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    logger.info("-" * 25)
    try:
        logger.debug("Agents (before update): {}".format(agents))
        _update_agents(kubernetes_conn, repo_manager_conn, agents)
        logger.info("Agents (after update): {}".format(agents))
        _apply_scaling_actions(agents)
    except KubernetesException as exc:
        logger.warning("Error from Kubernetes: {}".format(exc.message))
        return
    except RepositoryManagerException as exc:
        logger.warning("Error from Repository Manager: {}".format(exc.message))
        return


def _update_agents(kubernetes_conn, repo_manager_conn, agents):
    """
    Update agents pulling currently active Smart Scalers on Kubernetes.
    :param kubernetes_conn: (SimpleConnection) the Kubernetes connection.
    :param repo_manager_conn: (SimpleConnection) the Kubernetes connection.
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    smart_scalers_all = smart_scalers_ctrl.get_all_smart_scalers(kubernetes_conn)

    smart_scalers_to_remove = list(agents.keys() - set(map(lambda x: x["name"], smart_scalers_all)))

    smart_scalers_to_add = list(filter(lambda x: x["name"] not in agents, smart_scalers_all))

    logger.debug("Smart Scaler(s) ALL: {}".format(smart_scalers_all))
    logger.debug("Smart Scaler(s) to remove: {}".format(smart_scalers_to_remove))
    logger.debug("Smart Scaler(s) to add: {}".format(smart_scalers_to_add))

    for smart_scaler_name in smart_scalers_to_remove:
        smart_scalers_ctrl.delete_local_smart_scaler(smart_scaler_name, agents)

    for smart_scaler in smart_scalers_to_add:
        smart_scalers_ctrl.add_local_smart_scaler(smart_scaler, kubernetes_conn, repo_manager_conn, agents)


def _apply_scaling_actions(agents):
    """
    Apply scaling actions provided by agents.
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    for agent in agents.values():
        agent.apply_scaling_action()