def generate_action_space(actions):
    """
    Get the action space, expressed as list of actions, for the given enumeration.
    :param actions: (Enum) actions.
    :return: (list(Enum)) the action space, expressed as list of actions.
    """
    return [action for action in actions]


if __name__ == "__main__":
    from common.model.ai.smart_scaling import SimpleScalingAction as ScalingAction
    print(generate_action_space(ScalingAction))