from services.common.model.resources.smart_scaler import SmartScalerResource as SmartScalerResource
import pickle
from services.common.util import mathutil
from services.common.util.json import SimpleJSONEncoder as JSONEncoder
from json import dumps as json_dumps
from json import loads as json_loads
from sys import maxsize as maxint
import logging


# Configure logger
logger = logging.getLogger(__name__)


class SmartScaler:
    """
    A smart scaler, leveraging QLearning.
    """

    def __init__(self, name=None, pod_name=None, min_replicas=0, max_replicas=maxint, agent=None):
        """
        Create a new Reinforcement Learning agent.
        :param name: (string) the Smart Scaler name (Default: None).
        :param pod_name: (string) the Pod name (Default: None).
        :param min_replicas: (integer) the minimum replication degree (Default: 0).
        :param max_replicas: (integer) the maximum replication degree (Default: maxint).
        :param agent: (SimpleQLearningAgent) the QLearning agent.
        """
        self.resource = SmartScalerResource(name, pod_name, min_replicas, max_replicas)
        self.agent = agent

    def map_state(self, replicas, utilization):
        """
        Get the state for the given status.
        :param replicas: (int) the number of replicas.
        :param utilization: (float) the utilization degree.
        :return: (ReplicationUtilizationState) the state.
        """
        return self.agent.states.map_status2state(replicas, utilization)

    def get_reward(self, curr_state):
        """
        Compute the reward for the given state.
        :param curr_state: (ReplicationUtilizationState) the current state.
        :return: (float) the reward
        """
        return self.agent.rewarding_function(curr_state)

    def get_replicas(self, curr_state, return_action=False):
        """
        Get the suggested replication degree.
        :param: curr_state (ReplicationUtilizationState) the current state.
        :param: return_action (bool) if True, return both the new replicas and action performed (Default: False)
        :return: if *return_action* is True, (replicas, action) ; only replicas, otherwise.
        """
        reward = self.get_reward(curr_state)

        self.agent.learn(reward, curr_state)

        next_action = self.agent.get_action(curr_state)
        new_replicas = curr_state.replicas + next_action.value
        next_replicas = mathutil.get_bounded(self.resource.min_replicas, self.resource.max_replicas, new_replicas)

        if not return_action:
            return next_replicas
        else:
            return next_replicas, next_action

    def save_experience(self, state, action):
        """
        Save the last experience.
        :param state: the current state.
        :param action: the last action.
        :return: None
        """
        self.agent.save_experience(state, action)

    def pretty(self):
        """
        Return the pretty string representation.
        :return: (string) the pretty string representation.
        """
        s = "{}".format(self.__class__.__name__)
        s += "\n\tName: {}".format(self.resource.name)
        s += "\n\tPodName: {}".format(self.resource.pod_name)
        s += "\n\tMinReplicas: {}".format(self.resource.min_replicas)
        s += "\n\tMaxReplicas: {}".format(self.resource.max_replicas)
        s += "\n\t{}".format(self.agent.pretty())
        return s

    def __eq__(self, other):
        """
        Test equality.
        :param other: (SmartScaler) the other instance.
        :return: True, if equality is satisfied; False, otherwise.
        """
        if not isinstance(other, SmartScaler):
            return False

        for attr_name_1, attr_val_1 in self.__dict__.items():
            for attr_name_2, attr_val_2 in other.__dict__.items():
                if attr_name_1 == attr_name_2:
                    if attr_val_1 != attr_val_2:
                        print("Not equal {}".format(attr_name_1))
                        return False
        return True
        #return self.__dict__ == other.__dict__

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "{}({},{})".format(self.__class__.__name__, self.resource, self.agent)

    def __repr__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return self.__dict__.__str__()

    def to_binarys(self):
        """
        Return the binary string representation.
        :return: the binary string representation.
        """
        return pickle.dumps(self)

    def to_jsons(self):
        """
        Return the JSON string representation.
        :return: the JSON string representation.
        """
        return json_dumps(self, cls=JSONEncoder)

    @staticmethod
    def from_binarys(binarys):
        """
        Parse a SmartScaler from a binary string.
        :param binarys: (string) the binary string to parse.
        :return: (SmartScaler) the parsed agent.
        """
        return pickle.loads(binarys)

    @staticmethod
    def from_jsons(json):
        """
        Parse a SmartScaler from a JSON string.
        :param json: (string) the JSON string to parse.
        :return: (SmartScaler) the parsed pod.
        """
        return SmartScaler.from_json(json_loads(json))

    @staticmethod
    def from_json(json):
        """
        Parse a SmartScaler from a JSON object.
        :param json: (JSONObject) the JSON object to parse.
        :return: (SmartScaler) the parsed pod.
        """
        smart_scaler = SmartScaler()
        for attr_name, attr_value in json.items():
            setattr(smart_scaler, attr_name, attr_value)
        return smart_scaler

