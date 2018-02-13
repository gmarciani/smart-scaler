import numpy as np
import itertools


def generate_space_replicas_utilization(min_replicas, max_replicas, granularity, precision=None):
    """
    Generate the state space, expressed as list of floats.
    :param min_replicas: (integer) the minimum replication degree.
    :param max_replicas: (integer) the maximum replication degree.
    :param granularity: (integer) the granularity of the utilization space.
    :param precision: (integer) the precision of the utilization space.
    :return: (list(tuple(replicas, utilization))) the state space, expressed as list of tuples.
    """
    replication_space = generate_space_range(min_replicas, max_replicas)
    utilization_space = generate_space_normalized(granularity, precision)
    return list(itertools.product(replication_space, utilization_space))


def generate_space_range(min_val, max_val):
    """
    Generate the state space, expressed as list of integer.
    :param min_val: (integer) the minimum value.
    :param max_val: (integer) the maximum value.
    :return: (list(integer)) the state space, expressed as list of integers.
    """
    return list(range(min_val, max_val + 1))


def generate_space_normalized(granularity, round=None):
    """
    Generate the state space, expressed as list of floats.
    :param granularity: (integer) the granularity of the state space.
    :return: (list(float)) the state space, expressed as list of floats.
    """
    space = np.linspace(1.0/granularity, 1.0, num=granularity)
    if round is not None:
        return np.around(space, decimals=round)
    else:
        return space


if __name__ == "__main__":
    s1 = generate_space_normalized(10)
    print(s1)

    s2 = generate_space_replicas_utilization(1, 10, 10)
    print(s2)