"""
The control layer for the Heapster management.
"""


from services.kubernetes_simulator.model.heapster import SimpleHeapsterRegistry as KubernetesHeapster
import logging


# Logging
logger = logging.getLogger(__name__)


# Constants
HEAPSTER = KubernetesHeapster()


def get_heapster():
    """
    Retrieve Kubernetes Heapster.
    :return: (dict) Kubernetes Heapster.
    """
    return HEAPSTER


def teardown_heapster(exc):
    """
    Teardown Kubernetes Heapster.
    :param exc: the exception passed by the middleware during teardown process.
    :return: None
    """
    pass
