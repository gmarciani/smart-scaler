import random
import logging


# Configure logger
logger = logging.getLogger(__name__)

REWARD_MAX = float("inf")
DEFAULT_Q_VALUE = 0.0

DEFAULT_ALPHA = 0.5
DEFAULT_GAMMA = 0.9
DEFAULT_EPSILON = 0.1


class SimpleQLearningAgent:
    """
    A Q-Learning Agent.
    """

    def __init__(self, states, actions, alpha=DEFAULT_ALPHA, gamma=DEFAULT_GAMMA, epsilon=DEFAULT_EPSILON):
        """
        Create a new Q-Learning agent.
        :param states: (list(object)) the list of state.
        :param actions: (list(object)) the list of actions.
        :param alpha: (float) the learning rate (Default: 0.5).
        :param gamma: (float) the discount factor (Default: 0.9).
        :param epsilon: (float) the exploration factor (Default: 0.1).
        """
        self.states = states
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.n_states = len(self.states)
        self.n_actions = len(self.actions)

        self.q_table = {}

        self._init_q_table()

    def _init_q_table(self):
        """
        Initialize the Q table.
        :return: (void)
        """
        for s in self.states:
            for a in self.actions:
                self.q_table[(s, a)] = DEFAULT_Q_VALUE

    def get_q_value(self, state, action):
        """
        Get the Q-value for the pair (state, action).
        :param state: (object) the state.
        :param action: (object) the action.
        :return: (float) the Q-value for the pair (state, action).
        """
        return self.q_table[(state, action)]

    def learn(self, state_1, action_1, reward, state_2):
        """
        Execute the learning step.
        Q(s, a) += alpha * (reward(s,a) + max(Q(s') - Q(s,a))
        Q(s, a) = (1-alpha) * Q(s, a) + alpha * (reward(s, a) + gamma * max_{a}(Q(s,a)))
        :param state_1: (object) the previous state.
        :param action_1: (object) the previous action.
        :param reward: (float) the reward for the pair (state_1, action_1).
        :param state_2: (object) the current state.
        :return:
        """
        curr_q_value = self.get_q_value(state_1, action_1)
        q_value_max = max([self.get_q_value(state_2, a) for a in self.actions])
        learned_value = reward + self.gamma * q_value_max
        self.q_table[(state_1, action_1)] = (1.0 - self.alpha) * curr_q_value + alpha * learned_value

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
            q_values = [self.get_q_value(state, a) for a in self.actions]  # Q values for current state
            max_q_value = max(q_values)  # maximum Q value for the current state
            if q_values.count(max_q_value) > 1:  # there is more than one suggested action
                best_actions_idx = [i for i in range(self.n_actions) if q_values[i] == max_q_value]
                next_action_idx = random.choice(best_actions_idx)
                next_action = self.actions[next_action_idx]

            else:  # there is one suggested action, only
                next_action_idx = q_values.index(max_q_value)
                next_action = self.actions[next_action_idx]

            logger.debug("exploitation for state={} :: {}".format(state, next_action))

        return next_action

    def pretty(self):
        """
        Return the pretty string representation.
        :return: (string) the pretty string representation.
        """
        string_q_table = " ".join(map(str, self.actions))
        string_q_table += "\n"
        for state in self.states:
            q_values = [self.get_q_value(state, action) for action in self.actions]
            string_q_table += "{} {}".format(str(state), " ".join(map(str, q_values)))
            string_q_table += "\n"

        return "QLearningAgent\n\tStates: {}\n\tActions: {}\n\tQTable:\n{}".format(self.states, self.actions, string_q_table)

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "QLearningAgent({},{},{},{},{})".format(self.states, self.actions, self.alpha, self.gamma, self.q_table)

    def __repr__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return self.__str__()


if __name__ == "__main__":
    states = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    actions = [-1, 0, 1]
    alpha = 0.5
    gamma = 0.5
    epsilon = 0.1
    agent = SimpleQLearningAgent(states, actions, alpha, gamma, epsilon)

    def compute_reward(curr_state):
        if curr_state > 0.5:
            reward = -100
        elif curr_state > 0.7:
            reward = -10000
        elif curr_state > 0.9:
            reward = -1000000
        else:
            reward = 1000
        return reward

    print(agent)
    print(agent.pretty())

    cnt = {}
    for state in states:
        for action in actions:
            cnt[(state,action)] = 0

    last_state = None
    last_action = None
    iterations = 1000
    for i in range(iterations):
        print("Iteration {}/{}".format(i, iterations))

        curr_state = random.choice(states)

        reward = compute_reward(curr_state)

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