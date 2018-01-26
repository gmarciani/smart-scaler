from datetime import datetime
from services.common.control import connections as conn_ctrl
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
    conn_ctrl.close_repository_connection()