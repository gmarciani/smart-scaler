from random import random


def reward_random(curr_state):
    """
    Compute the reward for the given state, according to policy 'RANDOM'.
    :param curr_state: (float) the current state.
    :return: (float) the reward.
    """
    return random()


def reward_naive(curr_state):
    """
    Compute the reward for the given state, according to policy 'NAIVE'.
    :param curr_state: (float) the current state.
    :return: (float) the reward.
    """
    if curr_state > 0.5:
        reward = -100
    elif curr_state > 0.7:
        reward = -10000
    elif curr_state > 0.9:
        reward = -1000000
    else:
        reward = 1000
    return reward
