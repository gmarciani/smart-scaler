from enum import Enum, unique
from functools import total_ordering


@total_ordering
class ScalingAction:
    """
    A simple scaling action.
    """

    def __init__(self, type, magnitude):
        """
        Create a new scaling action.
        :param type: (SimpleScalingAction) the type of scaling.
        :param magnitude: (float) the magnitude of scaling.
        """
        self.type = type
        self.value = type.value * magnitude

    def __eq__(self, other):
        """
        Equality operator.
        :param other: the other object to compare.
        :return: True, if self is equal to other; False, otherwise.
        """
        return self.type == other.type and self.value == other.value

    def __lt__(self, other):
        """
        Less-than operator.
        :param other: the other object to compare.
        :return: True, if self is less than other; False, otherwise.
        """
        return self.value < other.value

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "({}[{}])".format(self.type.name, self.value)

    def __repr__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return self.__str__()

    def __hash__(self):
        """
        Return the hash representation.
        :return: (string) the hash representation.
        """
        return hash(self.type) ^ hash(self.value)

@unique
@total_ordering
class SimpleScalingAction(Enum):
    """
    Simple action space for scaling.
    *NO_SCALE* is used to mean that no replication should be added.
    *SCALE_IN* is used to mean that one replication should be removed.
    *SCALE_OUT* is used to mean that one replication should be added.
    """
    SCALE_IN = -1
    NO_SCALE = 0
    SCALE_OUT = 1

    def __lt__(self, other):
        """
        Less-than operator.
        :param other: the other object to compare.
        :return: True, if self is less than other; False, otherwise.
        """
        return self.value < other.value

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