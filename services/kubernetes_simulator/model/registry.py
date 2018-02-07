"""
Simulation of Kubernetes registry.
"""


class SimpleKubernetesRegistry:
    """
    A simple Kubernetes registry.
    """

    def __init__(self):
        """
        Create a new Kubernetes registry.
        """
        self._pods = {}
        self._smart_scalers = {}

    def get_pods(self):
        """
        Retrieve pods.
        :return: pods.
        """
        return self._pods

    def get_smart_scalers(self):
        """
        Retrieve smart scalers.
        :return: smart scalers.
        """
        return self._smart_scalers