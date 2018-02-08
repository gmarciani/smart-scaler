from flask import g
from services.kubernetes_simulator.model.heapster import SimpleKubernetesHeapster as KubernetesHeapster


HEAPSTER = KubernetesHeapster()


def get_heapster():
    """
    Retrieve Kubernetes Heapster.
    :return: (dict) Kubernetes Heapster.
    """
    return HEAPSTER
    #registry = getattr(g, "_registry", None)
    #if registry is None:
    #    registry = g._registry = __init_registry()
    #return registry


def teardown_heapster():
    """
    Teardown Kubernetes Heapster.
    :return: None
    """
    pass
    #registry = getattr(g, "_registry", None)
    #if registry is not None:
    #    setattr(g, "_registry", None)


def __init_registry():
    """
    Create a new instance of Kubernetes Heapster.
    :return: a new instance of Kubernetes Heapster.
    """
    return KubernetesHeapster()