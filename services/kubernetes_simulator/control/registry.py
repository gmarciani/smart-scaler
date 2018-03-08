from services.kubernetes_simulator.model.registry import SimpleKubernetesRegistry as KubernetesRegistry
import logging

# Configure logger
logger = logging.getLogger(__name__)


REGISTRY = KubernetesRegistry()


def get_registry():
    """
    Retrieve the registry.
    :return: (dict) the registry.
    """
    #logger.info("Getting Registry")
    return REGISTRY
    #registry = getattr(g, "_registry", None)
    #if registry is None:
    #    registry = g._registry = registry_connect()
    #return registry


def teardown_registry(exc):
    """
    Teardown the registry.
    :param exc: the exception passed by the middleware during teardown process.
    :return: (void)
    """
    #logger.debug("Tearing down Registry")
    pass
    #registry = getattr(g, "_registry", None)
    #if registry is not None:
    #   registry.close()
