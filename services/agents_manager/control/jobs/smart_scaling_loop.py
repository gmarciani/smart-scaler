from flask import current_app
from services.common.model.exceptions.kubernetes_exception import KubernetesException
from services.common.model.exceptions.repo_manager_exception import RepositoryException
from services.common.control import connections as connections_ctrl
from apscheduler.triggers.interval import IntervalTrigger
from services.agents_manager.control import agents_registry as agents_registry_ctrl
from services.agents_manager.control import smart_scalers as smart_scalers_ctrl
from services.common.model.scheduler import SimpleJob as SchedulerJob
import logging


logger = logging.getLogger(__name__)


def smart_scaling_loop_job(ctx):
    """
    Create the scheduler job 'smart_scaling_loop'.
    :param ctx: the application context.
    :return: the scheduler job.
    """
    with ctx:
        job = SchedulerJob(name="agents_update_loop", func=smart_scaling_loop, kwargs=dict(ctx=ctx),
                        trigger=IntervalTrigger(seconds=current_app.config["KUBERNETES_PULL"]))
    return job


def smart_scaling_loop(ctx):
    """
    Execute the smart scaling loop, i.e. update agents and apply scaling actions on Kubernetes.
    :param ctx: the application context.
    :return: None
    """
    logger.info("-" * 25)

    with ctx:
        kubernetes_conn = connections_ctrl.get_service_connection("kubernetes")
        repository_conn = connections_ctrl.get_service_connection("repository")

    agents = agents_registry_ctrl.get_local_registry()

    try:
        logger.debug("Agents (before update): {}".format(agents))
        smart_scalers_ctrl.update_registry(agents, kubernetes_conn, repository_conn)
        logger.info("Agents (after update): {}".format(agents))
        for agent in agents.values():
            smart_scalers_ctrl.apply_scaling(agent, kubernetes_conn)
            smart_scalers_ctrl.backup_agent(agent, repository_conn)
    except KubernetesException as exc:
        logger.warning("Error from Kubernetes: {}".format(exc.message))
        return
    except RepositoryException as exc:
        logger.warning("Error from Repository: {}".format(exc.message))
        return