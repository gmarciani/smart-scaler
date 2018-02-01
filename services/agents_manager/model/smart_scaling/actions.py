from enum import Enum, unique
from functools import total_ordering


def generate_action_space(actions):
    """
    Get the action space, expressed as list of actions, for the given enumeration.
    :param actions: (Enum) actions.
    :return: (list(Enum)) the action space, expressed as list of actions.
    """
    return [action for action in actions]


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
        if self.__class__ is not other.__class__:
            raise TypeError
        return self.name < other.name

    def __str__(self):
        return self.name


if __name__ == "__main__":
    print(generate_action_space(SimpleScalingAction))
    print(sorted(set(generate_action_space(SimpleScalingAction))))