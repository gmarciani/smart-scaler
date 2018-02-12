class PodResource:
    """
    The resource 'Pod' in Kubernetes Registry.
    """

    def __init__(self, name, replicas=1, cpu_utilization=0.0):
        """
        Create a new Pod.
        :param name: (string) the pod name.
        :param replicas: (integer) the replication degree.
        """
        self.name = name
        self.replicas = replicas
        self.cpu_utilization = cpu_utilization

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "Pod({},{})".format(self.name, self.replicas, self.cpu_utilization)

    def __repr__(self):
        """
        Return the representation.
        :return: (string) the representation.
        """
        return self.__dict__.__str__()

    @staticmethod
    def from_json(json):
        name = json["name"]
        replicas = json["replicas"] if "replicas" in json else 1
        cpu_utilization = json["cpu_utilization"] if "utilization" in json else 0.0
        return PodResource(name=name, replicas=replicas, cpu_utilization=cpu_utilization)


if __name__ == "__main__":
    from services.common.util.json import MyJSONEncoder
    import json

    pod = PodResource("my-pod-1")

    json_string = json.dumps(pod, cls=MyJSONEncoder)
    json_object = json.loads(json_string)
    pod2 = PodResource.from_json(json_object)

    print(pod)
    print(pod2)