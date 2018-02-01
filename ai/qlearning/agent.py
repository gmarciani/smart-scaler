from ai.qlearning import rewarding
from services.common.util import formatutil
import random
import itertools
import logging


# Configure logger
logger = logging.getLogger(__name__)

REWARD_MAX = float("inf")
DEFAULT_Q_VALUE = 0.0

DEFAULT_REWARDING_FUNCTION = rewarding.stupid_rewarding_function


class SimpleQLearningAgent:
    """
    A Q-Learning Agent.
    """

    def __init__(self, states, actions, alpha, gamma, epsilon, rewarding_function=DEFAULT_REWARDING_FUNCTION):
        """
        Create a new Q-Learning agent.
        :param states: (iterable(object)) the state space.
        :param actions: (iterable(object)) the action space.
        :param alpha: (float) the qlearning rate (Typical: 0.5).
        :param gamma: (float) the discount factor (Typical: 0.9).
        :param epsilon: (float) the exploration factor (Typical: 0.1).
        :param rewarding_function: (function) the rewardng function (Default: reward_utils.simple_rewarding).
        """
        self.states = states
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.rewarding_function = rewarding_function

        self.qtable = {(s,a): DEFAULT_Q_VALUE for s,a in itertools.product(self.states, self.actions)}

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

    def learn(self, state_1, action_1, reward, state_2):
        """
        Execute the qlearning step.
        Q(s, a) += alpha * (reward(s,a) + max(Q(s') - Q(s,a))
        Q(s, a) = (1-alpha) * Q(s, a) + alpha * (reward(s, a) + gamma * max_{a}(Q(s,a)))
        :param state_1: (object) the previous state.
        :param action_1: (object) the previous action.
        :param reward: (float) the reward for the pair (state_1, action_1).
        :param state_2: (object) the current state.
        :return:
        """
        curr_qvalue = self.get_qvalue(state_1, action_1)
        max_qvalue = max([self.get_qvalue(state_2, a) for a in self.actions])
        learned_value = reward + self.gamma * max_qvalue
        self.qtable[(state_1, action_1)] = (1.0 - self.alpha) * curr_qvalue + self.alpha * learned_value

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
        return self.__str__()


if __name__ == "__main__":
    states = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    actions = [-1, 0, 1]
    alpha = 0.5
    gamma = 0.5
    epsilon = 0.1
    rewarding_function = rewarding.stupid_rewarding_function
    agent = SimpleQLearningAgent(states, actions, alpha, gamma, epsilon, rewarding_function)

    print(agent)
    print(agent.pretty())

    cnt = {}
    for state in states:
        for action in actions:
            cnt[(state,action)] = 0

    last_state = None
    last_action = None
    iterations = 10
    for i in range(iterations):
        print("Iteration {}/{}".format(i, iterations))

        curr_state = random.choice(states)

        reward = agent.get_reward(curr_state)

        print("State={} | Reward={}".format(curr_state, reward))

        if last_state is not None:
            agent.learn(last_state, last_action, reward, curr_state)

        action = agent.get_action(curr_state)

        print("State={} | Reward={} | Action={}".format(curr_state, reward, action))

        cnt[(curr_state,action)] += 1

        last_state = curr_state
        last_action = action

        print(agent.pretty())

        print("-" * 15)

    for state in states:
        for action in actions:
            print("{} => {} : {}".format(state, action, cnt[(state, action)]))