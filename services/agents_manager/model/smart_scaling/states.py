import numpy as np
import itertools


class ReplicationUtilizationSpace:

    def __init__(self, min_replicas, max_replicas, granularity, round=None):
        """
        Create a new state whose dimensions are replications and utilization.
        :param min_replicas: (integer) the minimum number of replicas.
        :param max_replicas: (integer) the maximum number of replicas.
        :param granularity: (integer) the granularity for the discretization of utilization.
        :param round: (integer) the number of decimal to round bounds.
        """
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.granularity = granularity

        self.replication_space = generate_space_range(min_replicas, max_replicas)
        self.utilization_space = generate_space_normalized(granularity, round)

        self.space = list(itertools.product(self.replication_space, self.utilization_space))

    def __iter__(self):
        """
        Initialize iterations.
        :return: (list) the space.
        """
        return self.space.__iter__()

    def __len__(self):
        """
        Get the space size.
        :return: (integer) the space size.
        """
        return self.space.__len__()

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "{}({},{},{},{},{})".format(self.__class__.__name__, self.min_replicas, self.max_replicas,
                                              self.granularity, self.replication_space, self.utilization_space)

    def __repr__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return self.__str__()


def generate_space_replicas_utilization(min_replicas, max_replicas, granularity, round=None):
    """
    Generate the state space, expressed as list of floats.
    :param min_replicas: (integer) the minimum replication degree.
    :param max_replicas: (integer) the maximum replication degree.
    :param granularity: (integer) the granularity of the utilization space.
    :return: (list(tuple(replicas, utilization))) the state space, expressed as list of tuples.
    """
    replication_space = generate_space_range(min_replicas, max_replicas)
    utilization_space = generate_space_normalized(granularity, round)
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

    s3 = ReplicationUtilizationSpace(1, 10, 10)
    print(s3)

    for state in s3:
        print(state)