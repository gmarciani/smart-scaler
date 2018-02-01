from agents_manager.model.learning.qlearning_agent import SimpleQLearningAgent as QLearningAgent
from agents_manager.model.smart_scaling import states
from agents_manager.model.smart_scaling import actions
from agents_manager.model.smart_scaling.actions import SimpleScalingAction as ScalingAction
from services.common.util import mathutil
from services.common.util import formatutil
import random
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


class SmartScalingAgentQLearning(QLearningAgent):
    """
    A Smart Scaling Agent, leveraging Q-Learning.
    """

    def __init__(self, name, pod_name, min_replicas, max_replicas, granularity,
                 alpha=DEFAULT_ALPHA, gamma=DEFAULT_GAMMA, epsilon=DEFAULT_EPSILON,
                 round=DEFAULT_ROUND):
        """
        Create a new Reinforcement Learning agent.
        :param name: (string) the Smart Scaler name.
        :param pod_name: (string) the Pod name.
        :param min_replicas: (integer) the minimum replication degree.
        :param max_replicas: (integer) the maximum replication degree.
        :param granularity: (integer) the granularity for utilization space.
        :param alpha: (float) the learning rate (Default: 0.5).
        :param gamma: (float) the discount factor (Default: 0.9).
        :param epsilon: (float) the exploration factor (Default: 0.1).
        :param round: (integer) the number of decimal to round bounds (Default: None).
        """
        QLearningAgent.__init__(self,
                                states.ReplicationUtilizationSpace(min_replicas, max_replicas, granularity, round),
                                actions.generate_action_space(ScalingAction),
                                alpha, gamma, epsilon)
        self.name = name
        self.pod_name = pod_name

    def map_state(self, replicas, utilization):
        """
        Get the state for the given status.
        :param replicas: (int) the number of replicas.
        :param utilization: (float) the utilization degree.
        :return: (tuple(replicas, utilization)) the state.
        """
        return (replicas, mathutil.get_upper_bound(self.states.utilization_space, utilization))

    def get_scaling(self, curr_state):
        """
        Get the suggested replication degree.
        :param: curr_state (tuple(replicas, utilization)) the current state.
        :return: (int) the suggested replication degree.
        """
        next_action = super().get_action(curr_state)
        curr_replicas = curr_state[0]
        new_replicas = curr_replicas + next_action.value
        min_replicas = self.states.replication_space.min_replicas
        min_replicas = self.states.replication_space.max_replicas

        next_replicas = max(min_replicas, min(max_replicas, new_replicas))
        return next_replicas

    def pretty(self):
        """
        Return the pretty string representation.
        :return: (string) the pretty string representation.
        """
        s = "SmartScalingAgent"
        s += "\n\tName: {}".format(self.name)
        s += "\n\tPodName: {}".format(self.pod_name)
        s += "\n\tMinReplicas: {}".format(self.states.min_replicas)
        s += "\n\tMaxReplicas: {}".format(self.states.max_replicas)
        s += "\n\tGranularity: {}".format(self.states.granularity)
        s += "\n\tStates: {}".format(self.states.space)
        s += "\n\tActions: {}".format([a.name for a in self.actions])
        s += "\n\tAlpha: {}".format(self.alpha)
        s += "\n\tGamma: {}".format(self.gamma)
        s += "\n\tEpsilon: {}".format(self.epsilon)
        s += "\n\tQTable:\n{}".format(formatutil.pprint_qtable(self.qtable))

        return s

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "{}({},{},{})".format(self.__class__.__name__, self.name, self.pod_name, QLearningAgent.__str__(self))

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
    ugran = 10
    alpha = 0.5
    gamma = 0.9
    epsilon = 0.1
    agent = SmartScalingAgentQLearning(name, podname, min_replicas, max_replicas, ugran, alpha, gamma, epsilon)

    print(agent)
    print(agent.pretty())

    