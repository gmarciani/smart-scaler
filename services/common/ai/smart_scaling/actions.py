from enum import Enum, unique
from functools import total_ordering

@unique
@total_ordering
class SimpleScalingAction(Enum):
    """
    Simple action space for scaling.
    *NO_SCALE* is used to mean that no replication should be added.
    *SCALE_IN* is used to mean that one replication should be removed.
    *SCALE_OUT* is used to mean that one replication should be added.
    """
    NO_SCALE = 0
    SCALE_IN = -1
    SCALE_OUT = 1

    def __lt__(self, other):
        """
        Less-than operator.
        :param other: the other object to compare.
        :return: True, if self is less than other; False, otherwise.
        """
        return self.name < other.name

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return self.name

    def __repr__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return self.__str__()


if __name__ == "__main__":
    print(sorted(set([action for action in SimpleScalingAction])))