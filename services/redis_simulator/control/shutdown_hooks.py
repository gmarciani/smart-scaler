from datetime import datetime
import logging


# Configure logger
logger = logging.getLogger(__name__)


def simple_shutdown_hook(param):
    """
    Perform all shutdown actions.
    :param param: (dict) dictionary of parameters.
    :return: (void)
    """
    logger.info("Shutdown Hook at {}: {}".format(datetime.now(), param))