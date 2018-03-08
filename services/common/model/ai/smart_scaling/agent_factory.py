"""
Factory methods to build QLearning agents for Smart Scalers.
"""
from services.common.model.ai.qlearning.qlearning_agent import QLearningAgent
from services.common.model.ai.smart_scaling.states import ReplicationUtilizationSpace
from services.common.model.ai.smart_scaling.actions_utils import generate_action_space_from_magnitude
from services.common.util.sysutil import import_string


def build(resource):
    """
    Build a smart scaling agent from a smart scaler resource.
    :param resource: (SmartScalerResource) a smart scaler resource.
    :return: (QLearningAgent) the agent.
    """
    states = ReplicationUtilizationSpace(resource.min_replicas, resource.max_replicas,
                                         resource.ai_params["state_granularity"],
                                         resource.ai_params["state_precision"])
    actions = generate_action_space_from_magnitude(resource.ai_params["action_magnitude"])
    alpha = resource.ai_params["alpha"]
    gamma = resource.ai_params["gamma"]
    epsilon = resource.ai_params["epsilon"]

    rewarding_function_import_name = "services.common.model.ai.smart_scaling.rewarding.{}".format(resource.ai_params["rewarding_function"])
    rewarding_function = import_string(rewarding_function_import_name)

    return QLearningAgent(
        states=states,
        actions=actions,
        alpha=alpha, gamma=gamma, epsilon=epsilon,
        rewarding_function=rewarding_function)