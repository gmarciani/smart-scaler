"""
The model that realizes a Heapster Registry.
"""


class SimpleHeapsterRegistry:
    """
    A simple implementation of a Heapster Registry.
    """

    def __init__(self):
        """
        Create a new instance of a Heapster Registry.

        Returns
        ----------
        SimpleHeapsterRegistry
            A new instance of a Heapster Registry.
        """
        self._pods = {}  # pod_name: dict

    def get_pod_metrics(self):
        """
        Retrieve all Pods metrics.

        Returns
        -------
        dict
            The dictionary containing all Pods metrics. Each Pod Metric is represented as a dictionary.
        """
        return self._pods