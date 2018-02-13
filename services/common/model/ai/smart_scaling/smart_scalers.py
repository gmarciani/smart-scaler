from services.common.model.ai.smart_scaling.smart_scaling_agent import SmartScalerQLearning


class SmartScalerQLearningRandom(SmartScalerQLearning):
    """
    A smart scaler that leverages Q-Learning with random rewarding function.
    """

    def __init__(self):
        """
        Create a new smart scaler.
        """
        SmartScalerQLearning.__init__(self, )