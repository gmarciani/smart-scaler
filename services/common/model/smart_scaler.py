import json

class SmartScaler:
    """
    A Kubernetes SmartScaler.
    """

    def __init__(self, name, pod_name, min_replicas=0, max_replicas=1):
        """
        Create a new Smart Scaler.
        :param name: (string) the Smart Scaler name.
        :param min_replicas: (integer) the minimum replication degree (default is 0).
        :param max_replicas: (integer) the maximum replication degree (default is 1).
        """
        self.name = name
        self.pod_name = pod_name
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "SmartScaler({},{})".format(self.name, self.pod_name, self.min_replicas, self.max_replicas)

    def __repr__(self):
        """
        Return the JSON representation.
        :return: (json) the JSON representation.
        """
        return self.__dict__