from enum import Enum, unique
from functools import total_ordering


@unique
@total_ordering
class AITechnique(Enum):
    """
    Techniques of Artificial Intelligence for Smart Scaling.
    """
    RANDOM = 1
    QLEARNING = 2

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