from services.common.model.ai.qlearning import rewarding
from services.common.util import formatutil
from services.common.util.json import AdvancedJSONEncoder as JSONEncoder
from json import dumps as json_dumps
from json import loads as json_loads
import random
import itertools
import logging
from services.common.util.sysutil import import_string as import_string
import pickle


# Configure logger
logger = logging.getLogger(__name__)

REWARD_MAX = float("inf")
DEFAULT_Q_VALUE = 0.0

DEFAULT_REWARDING_FUNCTION = rewarding.stupid_rewarding_function


class SimpleQLearningAgent:
    """
    A Q-Learning Agent.
    """

    def __init__(self, states=None, actions=None, alpha=0.5, gamma=0.9, epsilon=0.1,
                 rewarding_function=DEFAULT_REWARDING_FUNCTION):
        """
        Create a new Q-Learning agent.
        :param states: (iterable(object)) the state space (Default: None).
        :param actions: (iterable(object)) the action space.
        :param alpha: (float) the qlearning rate (Default: 0.5).
        :param gamma: (float) the discount factor (Default: 0.9).
        :param epsilon: (float) the exploration factor (Default: 0.1).
        :param rewarding_function: (function|string) the rewarding function (Default: reward_utils.simple_rewarding).
        """
        self.states = states
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.rewarding_function = import_string(rewarding_function) if isinstance(rewarding_function,
                                                                                  str) else rewarding_function

        self.qtable = {(s, a): DEFAULT_Q_VALUE for (s, a) in itertools.product(self.states, self.actions)}

        self.last_state = None
        self.last_action = None

    def get_reward(self, curr_state):
        """
        Compute the reward for the given state.
        :param curr_state: (ReplicationUtilizationState) the current state.
        :return: (float) the reward
        """
        return self.rewarding_function(curr_state)

    def get_qvalue(self, state, action):
        """
        Get the Q-value for the pair (state, action).
        :param state: (object) the state.
        :param action: (object) the action.
        :return: (float) the Q-value for the pair (state, action).
        """
        return self.qtable[(state, action)]

    def learn(self, reward, state_2):
        """
        Execute the qlearning step.
        Q(s, a) += alpha * (reward(s,a) + max(Q(s') - Q(s,a))
        Q(s, a) = (1-alpha) * Q(s, a) + alpha * (reward(s, a) + gamma * max_{a}(Q(s,a)))
        :param reward: (float) the reward for the pair (state_1, action_1).
        :param state_2: (object) the current state.
        :return: None
        """
        if self.last_state is None:
            return
        curr_qvalue = self.get_qvalue(self.last_state, self.last_action)
        max_qvalue = max([self.get_qvalue(state_2, a) for a in self.actions])
        learned_value = reward + self.gamma * max_qvalue
        self.qtable[(self.last_state, self.last_action)] = (1.0 - self.alpha) * curr_qvalue + self.alpha * learned_value

    def get_action(self, state):
        """
        Get the suggested action for the given state.
        :param state: (object) the current state.
        :return: (object) the suggested action for the given state.
        """
        # exploration vs exploitation
        should_explore = random.random() < self.epsilon

        # if exploration...
        if should_explore:
            next_action = random.choice(self.actions)
            logger.debug("exploration for state={} :: {}".format(state, next_action))

        # if exploitation...
        else:
            qvalues = [self.get_qvalue(state, a) for a in self.actions]  # Q values for current state
            max_qvalue = max(qvalues)  # maximum Q value for the current state
            if qvalues.count(max_qvalue) > 1:  # there is more than one suggested action
                best_actions_idx = [i for i in range(len(self.actions)) if qvalues[i] == max_qvalue]
                next_action_idx = random.choice(best_actions_idx)
                next_action = self.actions[next_action_idx]

            else:  # there is one suggested action, only
                next_action_idx = qvalues.index(max_qvalue)
                next_action = self.actions[next_action_idx]

            logger.debug("exploitation for state={} :: {}".format(state, next_action))

        return next_action

    def save_experience(self, state, action):
        """
        Save the last experience.
        :param state: the current state.
        :param action: the last action.
        :return: None
        """
        self.last_state = state
        self.last_action = action

    def pretty(self):
        """
        Return the pretty string representation.
        :return: (string) the pretty string representation.
        """
        s = "{}".format(self.__class__.__name__)
        s += "\n\tStates: {}".format(self.states)
        s += "\n\tActions: {}".format(self.actions)
        s += "\n\tAlpha: {}".format(self.alpha)
        s += "\n\tGamma: {}".format(self.gamma)
        s += "\n\tEpsilon: {}".format(self.epsilon)
        s += "\n\tRewarding: {}".format(self.rewarding_function.__module__+"."+self.rewarding_function.__name__)
        s += "\n\tQTable:\n{}".format(formatutil.pprint_qtable(self.qtable))
        return s

    def __eq__(self, other):
        """
        Test equality.
        :param other: (SimpleQLearningAgent) the other instance.
        :return: True, if equality is satisfied; False, otherwise.
        """
        if not isinstance(other, SimpleQLearningAgent):
            return False
        return self.__dict__ == other.__dict__

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "{}({},{},{},{},{},{},{})".format(self.__class__.__name__, self.states, self.actions, self.alpha,
                                                 self.gamma, self.epsilon, self.rewarding_function, self.qtable)

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
        Parse a SimpleQLearningAgent from a binary string.
        :param binarys: (string) the binary string to parse.
        :return: (SimpleQLearningAgent) the parsed agent.
        """
        return pickle.loads(binarys)

    @staticmethod
    def from_jsons(json):
        """
        Parse a SimpleQLearningAgent from a JSON string.
        :param json: (string) the JSON string to parse.
        :return: (SimpleQLearningAgent) the parsed agent.
        """
        return SimpleQLearningAgent.from_json(json_loads(json))

    @staticmethod
    def from_json(json):
        """
        Parse a SimpleQLearningAgent from a JSON object.
        :param json: (JSONObject) the JSON object to parse.
        :return: (SimpleQLearningAgent) the parsed agent.
        """
        agent = SimpleQLearningAgent()
        for attr_name, attr_value in json.items():
            setattr(agent, attr_name, attr_value)
        return agent
