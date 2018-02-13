from services.common.util.json import SimpleJSONEncoder as JSONEncoder
from json import dumps as json_dumps
from json import loads as json_loads
from sys import maxsize as maxint


class SmartScalerResource:
    """
    The resource 'SmartScaler' in Kubernetes Registry.
    """

    def __init__(self, name=None, pod_name=None, min_replicas=0, max_replicas=maxint):
        """
        Create a new smart scaler.
        :param name: (string) the name of the smart scaler (Default: None).
        :param pod_name: (string) the name of the managed pod (Default: None).
        :param min_replicas: (integer) the minimum replication degree (Default: 0).
        :param max_replicas: (integer) the maximum replication degree (Default: sys.maxsize).
        """
        self.name = name
        self.pod_name = pod_name
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas

    def __eq__(self, other):
        """
        Test equality.
        :param other: (PodResource) the other instance.
        :return: True, if equality is satisfied; False, otherwise.
        """
        if not isinstance(other, SmartScalerResource):
            return False
        return self.__dict__ == other.__dict__

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "{}({},{})".format(self.__class__.__name__, self.name, self.pod_name, self.min_replicas, self.max_replicas)

    def __repr__(self):
        """
        Return the representation.
        :return: (string) the representation.
        """
        return self.__dict__.__str__()

    def to_jsons(self):
        """
        Return the JSON string representation.
        :return: the JSON string representation.
        """
        return json_dumps(self, cls=JSONEncoder)

    @staticmethod
    def from_jsons(json):
        """
        Parse a SmartScalerResource from a JSON string.
        :param json: (string) the JSON string to parse.
        :return: (SmartScalerResource) the parsed pod.
        """
        return SmartScalerResource.from_json(json_loads(json))

    @staticmethod
    def from_json(json):
        """
        Parse a SmartScalerResource from a JSON object.
        :param json: (JSONObject) the JSON object to parse.
        :return: (SmartScalerResource) the parsed smart scaler.
        """
        smart_scaler = SmartScalerResource()
        for attr_name, attr_value in json.items():
            setattr(smart_scaler, attr_name, attr_value)
        return smart_scaler



