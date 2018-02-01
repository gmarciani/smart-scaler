from functools import total_ordering
from services.agents_manager.model.smart_scaling import states_utils
import itertools


@total_ordering
class ReplicationUtilizationState:

    def __init__(self, replicas, utilization):
        """
        Create a new state.
        :param replicas: (int) the number of replicas.
        :param utilization: (float) the utilization degree in [0.0, 1.0]
        """
        self.replicas = replicas
        self.utilization = utilization

    def __lt__(self, other):
        """
        Less-than operator.
        :param other: the other object to compare.
        :return: True, if self is less than other; False, otherwise.
        """
        return self.replicas < other.replicas if self.replicas != other.replicas else self.utilization < other.utilization

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "({},{})".format(self.replicas, round(self.utilization, 5))

    def __repr__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return self.__str__()


class ReplicationUtilizationSpace:

    def __init__(self, min_replicas, max_replicas, granularity, round=None):
        """
        Create a new state whose dimensions are replications and utilization.
        :param min_replicas: (integer) the minimum number of replicas.
        :param max_replicas: (integer) the maximum number of replicas.
        :param granularity: (integer) the granularity for the discretization of utilization.
        :param round: (integer) the number of decimal to round bounds.
        """
        self.replication_space = states_utils.generate_space_range(min_replicas, max_replicas)
        self.utilization_space = states_utils.generate_space_normalized(granularity, round)

        self.space = list(ReplicationUtilizationState(r, u) for (r,u) in itertools.product(self.replication_space, self.utilization_space))

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
        return "{}({},{})".format(self.__class__.__name__, self.replication_space, self.utilization_space)

    def __repr__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return self.__str__()


if __name__ == "__main__":
    s3 = ReplicationUtilizationSpace(1, 10, 10)
    print(s3)

    for state in s3:
        print(state)