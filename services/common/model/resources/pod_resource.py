from services.common.util.jsonutil import AdvancedJSONEncoder as JSONEncoder
from json import dumps as json_dumps
from json import loads as json_loads


class PodResource:
    """
    The resource 'Pod' in Kubernetes Registry.
    """

    def __init__(self, name=None, replicas=1, cpu_utilization=0.0):
        """
        Create a new Pod.
        :param name: (string) the pod name (Default: None).
        :param replicas: (integer) the replication degree (Default: 1).
        :param cpu_utilization: (float) the CPU utilization (Default: 0.0).
        """
        self.name = name
        self.replicas = replicas
        self.cpu_utilization = cpu_utilization

    def __eq__(self, other):
        """
        Test equality.
        :param other: (PodResource) the other instance.
        :return: True, if equality is satisfied; False, otherwise.
        """
        if not isinstance(other, PodResource):
            return False
        return self.__dict__ == other.__dict__

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "{}({},{})".format(self.__class__.__name__, self.name, self.replicas, self.cpu_utilization)

    def __repr__(self):
        """
        Return the representation.
        :return: (string) the representation.
        """
        return self.__dict__.__str__()

    def to_json(self):
        """
        Return the JSON object representation.
        :return: the JSON object representation.
        """
        return vars(self)

    def to_jsons(self):
        """
        Return the JSON string representation.
        :return: the JSON string representation.
        """
        return json_dumps(self, cls=JSONEncoder)

    @staticmethod
    def from_jsons(json):
        """
        Parse a PodResource from a JSON string.
        :param json: (string) the JSON string to parse.
        :return: (PodResource) the parsed pod.
        """
        return PodResource.from_json(json_loads(json))

    @staticmethod
    def from_json(json):
        """
        Parse a PodResource from a JSON object.
        :param json: (JSONObject) the JSON object to parse.
        :return: (PodResource) the parsed pod.
        """
        pod = PodResource()
        for attr_name, attr_value in json.items():
            setattr(pod, attr_name, attr_value)
        return pod