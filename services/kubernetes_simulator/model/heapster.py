"""
Simulation of Kubernetes Heapster.
"""


class SimpleKubernetesHeapster:
    """
    A simple Kubernetes Heapster.
    """

    def __init__(self):
        """
        Create a new Kubernetes Heapster.
        """
        self._pods = {}

    def get_pod_metrics(self):
        """
        Retrieve metrics for Pods.
        :return: metrics for Pods.
        """
        return self._pods