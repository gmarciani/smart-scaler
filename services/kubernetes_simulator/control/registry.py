from flask import g
from services.kubernetes_simulator.model.registry import SimpleKubernetesRegistry as KubernetesRegistry


REGISTRY = KubernetesRegistry()


def get_registry():
    """
    Retrieve the registry.
    :return: (dict) the registry.
    """
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
    pass
    #registry = getattr(g, "_registry", None)
    #if registry is not None:
    #   registry.close()
