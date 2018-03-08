from services.common.model.ai.ai_techniques import AITechnique
from services.common.model.ai.smart_scaling.smart_scaling_agent import SmartScalerQLearning
import logging

# Configure logger
logger = logging.getLogger(__name__)


def create(resource):
    """
    Create a new smart scaler for the given resource.
    :param resource: (SmartScalerResource) the smart scaler resource.
    :return: (SmartScaler) the smart scaler.
    """
    ai_technique = AITechnique[resource.ai_technique]

    logger.debug("Creating a smart scaler with AI technique {}".format(ai_technique.name))

    if ai_technique is AITechnique.QLEARNING:
        logger.debug("Creating a smart scaler with AI technique {}".format(ai_technique.name))
        scaler = SmartScalerQLearning(resource)
    else:
        raise ValueError("Cannot instantiate smart scaler with AI technique {}".format(ai_technique.name))

    return scaler