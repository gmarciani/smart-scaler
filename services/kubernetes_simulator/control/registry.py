"""
The control layer for the Kubernetes Registry management.
"""


from services.kubernetes_simulator.model.registry import SimpleKubernetesRegistry as KubernetesRegistry
import logging


# Logging
logger = logging.getLogger(__name__)


# Constants
REGISTRY = KubernetesRegistry()


def get_registry():
    """
    Retrieve the Kubernetes Registry.

    Returns
    -------
    SimpleKubernetesRegistry
        The Kubernetes Registry.
    """
    return REGISTRY


def teardown_registry(e):
    """
    Teardown the Kubernetes Registry.

    Parameters
    ----------
    e : Exception
        The exception passed by the middleware during teardown process.
    """
    pass
