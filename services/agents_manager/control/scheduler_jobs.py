"""
Scheduler jobs to synchronize the local Agents Manager Registry with the remote Kubernetes Registry.
"""


from flask import current_app
from services.common.model.exceptions.service_exception import KubernetesException
from services.common.control import connections as connections_ctrl
from apscheduler.triggers.interval import IntervalTrigger
from services.agents_manager.control import registry as registry_ctrl
from services.common.model.environment.scheduler import SimpleSchedulerJob as SchedulerJob
import logging


# Logging
logger = logging.getLogger(__name__)


def registry_sync_job(ctx):
    """
    Create the scheduler job for the function 'registry_sync_loop'.
    :param ctx: the application context.
    :return: the scheduler job.
    """
    with ctx:
        job = SchedulerJob(name="registry_sync", func=registry_sync, kwargs=dict(ctx=ctx),
                           trigger=IntervalTrigger(seconds=current_app.config["KUBERNETES_PULL"]))
    return job


def registry_sync(ctx):
    """
    Execute the registry sync function.
    :param ctx: the application context.
    :return: None
    """
    logger.info("-" * 25)

    with ctx:
        kubernetes_conn = connections_ctrl.get_connection("kubernetes")

    local_registry = registry_ctrl.get_local_registry()

    try:
        logger.debug("Smart scalers (before update): {}".format(local_registry))
        registry_ctrl.update_registry(local_registry, kubernetes_conn)
        logger.debug("Smart scalers (after update): {}".format(local_registry))
    except KubernetesException as exc:
        logger.warning("Error from Kubernetes: {}".format(exc.message))
        return