import json

class Pod:
    """
    A Kubernetes Pod.
    """

    def __init__(self, name, replicas=1):
        """
        Create a new Pod.
        :param name: (string) the pod name.
        :param replicas: (integer) the replication degree.
        """
        self.name = name
        self.replicas = replicas

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "Pod({},{})".format(self.name, self.replicas)

    def __repr__(self):
        """
        Return the JSON representation.
        :return: (json) the JSON representation.
        """
        return self.__dict__