from services.common.model.ai.smart_scaling.actions import SimpleScalingAction, ScalingAction


def generate_action_space(actions):
    """
    Get the action space, expressed as list of actions, for the given enumeration.
    :param actions: (Enum) actions.
    :return: (list(Enum)) the action space, expressed as list of actions.
    """
    return [action for action in actions]


def generate_action_space_from_magnitude(magnitude):
    """
    Get the action space, expressed as list of actions, according to the specified magnitude.
    :param magnitude: (int) the magnitude of scaling actions.
    :return: (list(ScalingAction)) the action space, expressed as list of scaling actions.
    """
    actions = set()

    for t in SimpleScalingAction:
        for m in range(1, magnitude + 1):
            a = ScalingAction(t, m)
            actions.add(a)

    return sorted(actions)