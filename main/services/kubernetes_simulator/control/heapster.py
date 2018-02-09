from flask import g
from services.kubernetes_simulator.model.heapster import SimpleKubernetesHeapster as KubernetesHeapster


HEAPSTER = KubernetesHeapster()


def get_heapster():
    """
    Retrieve Kubernetes Heapster.
    :return: (dict) Kubernetes Heapster.
    """
    return HEAPSTER
    #heapster = getattr(g, "_heapster", None)
    #if heapster is None:
    #    heapster = g._heapster = heapster_connect()
    #return heapster


def teardown_heapster(exc):
    """
    Teardown Kubernetes Heapster.
    :param exc: the exception passed by the middleware during teardown process.
    :return: None
    """
    pass
    #heapster = getattr(g, "_heapster", None)
    #if heapster is not None:
    #   heapster.close()
