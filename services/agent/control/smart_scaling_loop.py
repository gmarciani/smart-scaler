from flask import current_app
from services.common.model.exceptions.service_exception import KubernetesException
from services.common.model.exceptions.service_exception import RepositoryException
from services.common.control import connections as connections_ctrl
from apscheduler.triggers.interval import IntervalTrigger
from services.agents_manager.control import registry as smart_scalers_ctrl
from services.common.model.environment.scheduler import SimpleSchedulerJob as SchedulerJob
import logging

# Configure logger
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
        kubernetes_conn = connections_ctrl.get_connection("kubernetes")
        repository_conn = connections_ctrl.get_connection("repository")

    local_registry = smart_scalers_ctrl.get_local_registry()

    try:
        logger.debug("Smart scalers (before update): {}".format(local_registry))
        smart_scalers_ctrl.update_registry(local_registry, kubernetes_conn, repository_conn)
        logger.debug("Smart scalers (after update): {}".format(local_registry))
    except KubernetesException as exc:
        logger.warning("Error from Kubernetes: {}".format(exc.message))
        return
    except RepositoryException as exc:
        logger.warning("Error from Repository: {}".format(exc.message))
        return