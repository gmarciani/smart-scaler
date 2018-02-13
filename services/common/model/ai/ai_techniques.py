from enum import Enum, unique, auto
from functools import total_ordering


@unique
@total_ordering
class AITechnique(Enum):
    """
    Techniques of Artificial Intelligence for Smart Scaling.
    *QLEARNING* is used to mean that no replication should be added.
    """
    QLEARNING = auto()
    QLEARNING_RND = auto()

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