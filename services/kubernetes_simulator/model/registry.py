"""
The model that realizes a Kubernetes Registry.
"""


class SimpleKubernetesRegistry:
    """
    A simple implementation of a Kubernetes Registry.
    """

    def __init__(self):
        """
        Create a new instance of a Kubernetes Registry.

        Returns
        ----------
        SimpleKubernetesRegistry
            A new instance of a Kubernetes Registry.
        """
        self._pods = {}
        self._smart_scalers = {}

    def get_pods(self):
        """
        Retrieve all Pods resources.

        Returns
        -------
        dict
            The dictionary of Pods resources (PodResource).
        """
        return self._pods

    def get_smart_scalers(self):
        """
        Retrieve all Smart Scaler resources.

        Returns
        -------
        dict
            The dictionary of Smart Scaler resources (SmartScalerResource).
        """
        return self._smart_scalers