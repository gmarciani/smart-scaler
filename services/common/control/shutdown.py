from datetime import datetime
import logging


# Configure logger
logger = logging.getLogger(__name__)


def goodbye():
    """
    Print the goodbye message.
    :return: None
    """
    logger.info("Goodbye")