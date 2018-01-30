import numpy as np


def generate_state_space_normalized(granularity):
    """
    Generate the state space, expressed as list of floats.
    :param granularity: (integer) the granularity of the state space.
    :return: (list(float)) the state space, expressed as list of floats.
    """
    return np.linspace(0.0, 0.9, granularity)


if __name__ == "__main__":
    print(generate_state_space_normalized(10))