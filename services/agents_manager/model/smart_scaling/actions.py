from enum import Enum, unique, auto


def generate_action_space(actions):
    """
    Get the action space, expressed as list of actions, for the given enumeration.
    :param actions: (Enum) actions.
    :return: (list(Enum)) the action space, expressed as list of actions.
    """
    return [action for action in actions]

@unique
class SimpleScalingAction(Enum):
    """
    Simple action space for scaling.
    *NO_SCALE* is used to mean that no replication should be added.
    *SCALE_OUT* is used to mean that one replication should be added.
    *SCALE_IN* is used to mean that one replication should be removed.
    """
    NO_SCALE = auto()
    SCALE_OUT = auto()
    SCALE_IN = auto()


if __name__ == "__main__":
    print(generate_action_space(SimpleScalingAction))