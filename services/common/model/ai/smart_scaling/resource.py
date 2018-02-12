class SimpleSmartScalerResource:
    """
    Information for the initialization of a smart scaler.
    """
    def __init__(self, name, pod_name, min_replicas, max_replicas):
        """
        Create a new Reinforcement Learning agent.
        :param name: (string) the Smart Scaler name.
        :param pod_name: (string) the Pod name.
        :param min_replicas: (integer) the minimum replication degree.
        :param max_replicas: (integer) the maximum replication degree.
        """
        self.name = name
        self.pod_name = pod_name
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas