class SmartScalerResource:
    """
    The resource 'SmartScaler' in Kubernetes Registry.
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
        Return the representation.
        :return: (string) the representation.
        """
        return self.__dict__.__str__()

    @staticmethod
    def from_json(json):
        name = json["name"]
        pod_name = json["pod_name"]
        min_replicas = json["min_replicas"] if "min_replicas" in json else 0
        max_replicas = json["max_replicas"] if "max_replicas" in json else 1
        return SmartScalerResource(
            name=name,
            pod_name=pod_name,
            min_replicas=min_replicas,
            max_replicas=max_replicas)


if __name__ == "__main__":
    from services.common.util.json import MyJSONEncoder
    import json

    smart_scaler = SmartScalerResource("my-smart-scaler-1", "my-pod-1")

    json_string = json.dumps(smart_scaler, cls=MyJSONEncoder)
    json_object = json.loads(json_string)
    smart_scaler2 = SmartScalerResource.from_json(json_object)

    print(smart_scaler)
    print(smart_scaler2)



