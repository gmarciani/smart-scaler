import math
import random
from control import kube


class RLAgent:
    """
    A Reinforcement Learning agent.
    """

    def __init__(self, name, pod_name, min_replicas=0, max_replicas=1):
        """
        Create a new Reinforcement Learning agent.
        :param name: (string) the Smart Scaler name.
        :param pod_name: (string) the Pod name.
        :param min_replicas: (integer) the minimum replication degree (default is 0).
        :param max_replicas: (integer) the maximum replication degree (default is 1).
        """
        self.name = name
        self.pod_name = pod_name
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas

    def compute_replicas(self, pod_status):
        cpu_utilization = pod_status["cpu_utilization"]

        if 0.0 <= cpu_utilization <= 0.40:
            return self.min_replicas
        elif 0.40 < cpu_utilization <= 0.80:
            return self.min_replicas + self.max_replicas
        else:
            return self.max_replicas

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "Agent({},{})".format(self.name, self.pod_name, self.min_replicas, self.max_replicas)

    def __repr__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return self.__str__()
