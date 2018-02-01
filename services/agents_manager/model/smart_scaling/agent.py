from agents_manager.model.learning.qlearning_agent import SimpleQLearningAgent as QLearningAgent
from agents_manager.model.smart_scaling import states, states_utils
from agents_manager.model.smart_scaling import actions, actions_utils
from agents_manager.model.smart_scaling.actions import SimpleScalingAction as ScalingAction
from services.common.util import mathutil
import logging


# Configure logger
logger = logging.getLogger(__name__)

DEFAULT_MIN_REPLICAS = 1
DEFAULT_MAX_REPLICAS = 10
DEFAULT_STATE_SPACE_GRANULARITY = 10

DEFAULT_ALPHA = 0.5
DEFAULT_GAMMA = 0.9
DEFAULT_EPSILON = 0.1

DEFAULT_ROUND = None


class SmartScaler:
    """
    A Smart Scaler, leveragin QLearning.
    """

    def __init__(self, name, pod_name, min_replicas, max_replicas, agent):
        """
        Create a new Reinforcement Learning agent.
        :param name: (string) the Smart Scaler name.
        :param pod_name: (string) the Pod name.
        :param min_replicas: (integer) the minimum replication degree.
        :param max_replicas: (integer) the maximum replication degree.
        :param agent: (SimpleQLearningAgent) the QLearning agent.
        """
        self.name = name
        self.pod_name = pod_name
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.agent = agent

    def map_state(self, replicas, utilization):
        """
        Get the state for the given status.
        :param replicas: (int) the number of replicas.
        :param utilization: (float) the utilization degree.
        :return: (tuple(replicas, utilization)) the state.
        """
        return (replicas, mathutil.get_upper_bound(self.agent.states.utilization_space, utilization))

    def get_scaling(self, curr_state):
        """
        Get the suggested replication degree.
        :param: curr_state (ReplicationUtilizationState) the current state.
        :return: (int) the suggested replication degree.
        """
        next_action = self.agent.get_action(curr_state)
        new_replicas = curr_state.replicas + next_action.value
        next_replicas = mathutil.get_bounded(self.min_replicas, self.max_replicas, new_replicas)
        return next_replicas

    def pretty(self):
        """
        Return the pretty string representation.
        :return: (string) the pretty string representation.
        """
        s = "{}".format(self.__class__.__name__)
        s += "\n\tName: {}".format(self.name)
        s += "\n\tPodName: {}".format(self.pod_name)
        s += "\n\tMinReplicas: {}".format(self.min_replicas)
        s += "\n\tMaxReplicas: {}".format(self.max_replicas)
        s += "\n\t{}".format(self.agent.pretty())

        return s

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "{}({},{},{},{},{})".format(self.__class__.__name__, self.name, self.pod_name, self.min_replicas,
                                           self.max_replicas, self.agent)

    def __repr__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return self.__str__()


if __name__ == "__main__":
    name = "ss_my_pod"
    podname = "my_pod"
    min_replicas = 1
    max_replicas = 10
    granularity = 10
    round=None
    alpha = 0.5
    gamma = 0.9
    epsilon = 0.1

    scaler = SmartScaler(name, podname, min_replicas, max_replicas, QLearningAgent(
        states.ReplicationUtilizationSpace(min_replicas, max_replicas, granularity, round),
        actions_utils.generate_action_space(ScalingAction),
        alpha, gamma, epsilon))

    print(scaler)
    print(scaler.pretty())

