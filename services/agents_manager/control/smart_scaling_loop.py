from flask import current_app
from services.common.model.exceptions.kubernetes_exception import KubernetesException
from services.common.model.exceptions.repository_exception import RepositoryException
from services.common.control import connections as connections_ctrl
from apscheduler.triggers.interval import IntervalTrigger
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

    smart_scalers = smart_scalers_ctrl.get_local_registry()

    try:
        logger.debug("Smart Scalers (before update): {}".format(smart_scalers))
        smart_scalers_ctrl.update_registry(smart_scalers, kubernetes_conn, repository_conn)
        logger.info("Smart Scalers (after update): {}".format(smart_scalers))
        for smart_scaler in smart_scalers.values():
            #TODO load only if local version is less than repository version
            #smart_scalers_ctrl.load_smart_scaler(smart_scaler, repository_conn)
            smart_scalers_ctrl.apply_scaling(smart_scaler, kubernetes_conn)
            #smart_scalers_ctrl.store_smart_scaler(smart_scaler, repository_conn)
    except KubernetesException as exc:
        logger.warning("Error from Kubernetes: {}".format(exc.message))
        return
    except RepositoryException as exc:
        logger.warning("Error from Repository: {}".format(exc.message))
        return