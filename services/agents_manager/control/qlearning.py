from services.agents_manager.model.qlearning import Action as QLearningAction
import logging


# Configure logger
logger = logging.getLogger(__name__)


def compute_reward(state_curr, state_prev):
    """
    Compute the reward.
    :param state_curr: the current Pod state.
    :param state_prev: the previous Pod state.
    :return: (float) the reward.
    """
    # TODO
    cpu_utilization_curr = state_curr["cpu_utilization"]
    cpu_utilization_prev = state_prev["cpu_utilization"] if state_prev is not None else 0.0

    reward = -(cpu_utilization_curr - cpu_utilization_prev)

    return reward


def compute_normalized_state(state):
    """
    Compute the normalized state.
    :param state: the current Pod state.
    :return: the normalized state.
    """
    # TODO
    cpu_utilization = state["cpu_utilization"]
    return cpu_utilization


def compute_action(state_idx, matrix):
    """
    Compute the replication degree.
    :param state_idx: (int) the current Pod state, as matrix integer.
    :param matrix: (QMatrix) the Q learning matrix.
    :return: (QLearningAction) the suggested action.
    """
    suggested_action_idx = None
    max_reward = -float("inf")

    for action_idx in range(3):
        reward = matrix[state_idx][action_idx]
        if reward > max_reward:
            max_reward = reward
            suggested_action_idx = action_idx

    return QLearningAction(suggested_action_idx)


if __name__ == "__main__":
    print(QLearningAction(1))