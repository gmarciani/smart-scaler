"""
The control layer for Redis Database management.
"""


from services.redis_simulator.model.database import SimpleRedisDatabase as RedisDatabase
import logging


# Logging
logger = logging.getLogger(__name__)


# Constants
DATABASE = RedisDatabase()


def get_database():
    """
    Retrieve the database.

    Returns
    -------
    : SimpleRedisDatabase
        The Redis Database.
    """
    return DATABASE


def teardown_database(e):
    """
    Teardown the database.

    Parameters
    ----------
    e : exc
        The exception passed by the middleware during teardown process.
    """
    pass




