from random import random


def reward_random(curr_state):
    """
    Compute the reward for the given state, according to policy 'RANDOM'.
    :param curr_state: (ReplicationUtilizationState) the current state.
    :return: (float) the reward.
    """
    return random()


def reward_naive(curr_state):
    """
    Compute the reward for the given state, according to policy 'NAIVE'.
    :param curr_state: (ReplicationUtilizationState) the current state.
    :return: (float) the reward.
    """
    replicas = curr_state.replicas
    utilization = curr_state.utilization

    if replicas == 1 and 0.0 <= utilization <= 0.5:
        return 10000
    else:
        if 0.9 < utilization <= 1.0:
            return -100000
        elif 0.8 < utilization <= 0.9:
            return -10000
        elif 0.7 < utilization <= 0.8:
            return -1000
        elif 0.6 < utilization <= 0.7:
            return -100
        elif 0.5 < utilization <= 0.6:
            return 10000
        elif 0.4 < utilization <= 0.5:
            return 10000
        elif 0.3 < utilization <= 0.4:
            return -100
        elif 0.2 < utilization <= 0.3:
            return -1000
        elif 0.1 < utilization <= 0.2:
            return -10000
        elif 0.0 <= utilization <= 0.1:
            return -100000
        else:
            return -1