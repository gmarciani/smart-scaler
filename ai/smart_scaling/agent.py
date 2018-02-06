from ai.qlearning.agent import SimpleQLearningAgent as QLearningAgent
from ai.smart_scaling import states
from ai.smart_scaling import actions_utils
from ai.smart_scaling import rewarding
from ai.smart_scaling.actions import SimpleScalingAction as ScalingAction
from services.common.util import mathutil
import random
import logging


# Configure logger
logger = logging.getLogger(__name__)


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

        self.last_state = None
        self.last_action = None

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

        if self.last_state is not None and self.last_action is not None:
            self.agent.learn(self.last_state, self.last_action, reward, curr_state)

        next_action = self.agent.get_action(curr_state)
        new_replicas = curr_state.replicas + next_action.value
        next_replicas = mathutil.get_bounded(self.min_replicas, self.max_replicas, new_replicas)

        self.last_state = curr_state
        self.last_action = next_action

        if not return_action:
            return next_replicas
        else:
            return next_replicas, next_action

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
    max_replicas = 5
    granularity = 5
    round=None
    alpha = 0.5
    gamma = 0.9
    epsilon = 0.1
    rewarding_function = rewarding.simple_rewarding

    scaler = SmartScaler(name, podname, min_replicas, max_replicas, QLearningAgent(
        states.ReplicationUtilizationSpace(min_replicas, max_replicas, granularity, round),
        actions_utils.generate_action_space(ScalingAction),
        alpha, gamma, epsilon, rewarding_function))

    print(scaler)
    print(scaler.pretty())

    states = scaler.agent.states
    actions = scaler.agent.actions

    cnt = {}
    for state in states:
        for action in actions:
            cnt[(state, action)] = 0

    pod_status = {
        "replicas": min_replicas,
        "utilization": 0.0
    }

    iterations = 1000
    for i in range(iterations):
        print("Iteration {}/{}".format(i, iterations))

        pod_status["utilization"] = random.random()

        curr_state = scaler.map_state(pod_status["replicas"], pod_status["utilization"])

        new_replicas, action = scaler.get_replicas(curr_state, return_action=True)

        pod_status["replicas"] = new_replicas

        cnt[(curr_state, action)] += 1

        print(scaler.pretty())

        print("-" * 15)

    #for state in scaler.agent.states:
    #    for action in scaler.agent.actions:
    #        print("{} => {} : {}".format(state, action, cnt[(state, action)]))

    print("PodStatus: ", pod_status)

