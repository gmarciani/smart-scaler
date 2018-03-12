"""
Scheduler jobs for service 'Agent'.
"""


from flask import current_app
from services.common.model.exceptions.service_exception import KubernetesException
from services.common.model.exceptions.service_exception import RepositoryException
from apscheduler.triggers.interval import IntervalTrigger
from services.agent.control import context as context_ctrl
from services.common.model.environment.scheduler import SimpleSchedulerJob as SchedulerJob
from services.common.control import kubernetes as kubernetes_ctrl
from services.common.control import redis_repo as repository_ctrl
from services.common.model.ai.smart_scaling import smart_scaler_factory
from redis_lock import AlreadyAcquired
from random import shuffle
import logging


# Logging
logger = logging.getLogger(__name__)


def agent_loop_job(ctx):
    """
    Create the scheduler job for the function 'agent_loop'.

    Parameters
    ----------
    ctx : ApplicationContext
        The Flask app context.

    Returns
    -------
    job : SchedulerJob
        The APScheduler job.
    """
    with ctx:
        job = SchedulerJob(name="agent_loop", func=agent_loop, kwargs=dict(ctx=ctx),
                           trigger=IntervalTrigger(seconds=current_app.config["KUBERNETES_PULL"]))
    return job


def agent_loop(ctx):
    """
    Execute the main loop for an Agent.

    Parameters
    ----------
    ctx : ApplicationContext
        The Flask app context.
    """
    logger.debug("-" * 25)

    with ctx:
        k = context_ctrl.get_kubernetes()
        r = context_ctrl.get_repository()
        auid = context_ctrl.get_auid()
        interval = current_app.config["KUBERNETES_PULL"]

    logger.debug("Smart Scaling loop for Agent [{}]".format(auid))

    try:

        # ==============================================================================================================
        # Smart Scaling
        # ==============================================================================================================
        ssr_kubernetes = kubernetes_ctrl.get_all_smart_scalers(k)
        shuffle(ssr_kubernetes)

        for ssr in ssr_kubernetes:
            lock = repository_ctrl.lock_smart_scaler(r, ssr.name, auid=auid, expire=interval)

            try:
                acquired = lock.acquire(blocking=False)
            except AlreadyAcquired:
                acquired = True

            if acquired:
                logger.debug("Lock acquired on Smart Scaler [{}]".format(ssr.name))

                ss = repository_ctrl.load_smart_scaler(r, ssr.name)
                if ss is None:
                    logger.debug("Smart Scaler [{}] not found on Repository".format(ssr.name))
                    ss = smart_scaler_factory.create(ssr)
                    logger.debug("Smart Scaler [{}] created".format(ssr.name))
                else:
                    logger.debug("Smart Scaler [{}] loaded from Repository".format(ssr.name))

                old_replicas, new_replicas = apply_scaling(k, ss)
                logger.info("Smart Scaler [{}] scaled Pod [{}] from [{}] to [{}]"
                            .format(ss.resource.name, ss.resource.pod_name, old_replicas, new_replicas))

                repository_ctrl.store_smart_scaler(r, ss)
                logger.debug("Smart Scaler [{}] stored on Repository".format(ssr.name))

                # the lock releasing is implicitly done with the lock TTL
                #lock.release()
                #logger.debug("Lock released on Smart Scaler [{}] by Agent [{}]".format(ssr.name, auid))
            else:
                #logger.debug("Smart Scaler [{}] managed by another Agent [{}]".format(ssr.name, lock.get_owner_id().decode("UTF-8")))
                logger.debug("Smart Scaler [{}] managed by another Agent".format(ssr.name))

        # ==============================================================================================================
        # Repository Reconciliation
        # ==============================================================================================================
        lock = repository_ctrl.lock_reconciliation(r, auid=auid, expire=interval)
        try:
            acquired = lock.acquire(blocking=False)
        except AlreadyAcquired:
            acquired = True

        if acquired:
            logger.debug("Lock acquired on Repository Reconciliation.")
            deleted = repository_ctrl.reconcile(r, list(res.name for res in ssr_kubernetes))
            logger.info("Repository Reconciliation: deleted {}".format(deleted))
            # the lock releasing is implicitly done with the lock TTL
            #lock.release()
            #logger.debug("Lock released on Repository Reconciliation by Agent [{}]".format(auid))
        else:
            #logger.debug("Repository Reconciliation managed by another Agent [{}]".format(lock.get_owner_id().decode("UTF-8")))
            logger.debug("Repository Reconciliation managed by another Agent")

    except KubernetesException as exc:
        logger.warning("Error from Kubernetes: {}".format(exc.message))
    except RepositoryException as exc:
        logger.warning("Error from Repository: {}".format(exc.message))


def apply_scaling(k, agent):
    """
    Apply scaling actions provided by agents.
    :param k: (SimpleConnection) the connection to Kubernetes.
    :param agent: the Smart Scaler agent.
    :return: (int,int) old replicas, new replicas.
    """
    pod_name = agent.resource.pod_name

    pod = kubernetes_ctrl.get_pod(k, pod_name)

    curr_state = agent.map_state(pod.replicas, pod.cpu_utilization)

    new_replicas = agent.get_replicas(curr_state)

    return kubernetes_ctrl.set_pod_replicas(k, pod_name, new_replicas)