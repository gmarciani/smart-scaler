"""
The control layer for the Redis Database management.
"""


from services.redis_simulator.model.database import SimpleRedisDatabase as RedisDatabase
import logging


# Logging
logger = logging.getLogger(__name__)


# Constants
DATABASE = RedisDatabase()


def get_database():
    """
    Retrieve the Redis Database.

    Returns
    -------
    SimpleRedisDatabase
        The Redis Database.
    """
    return DATABASE


def teardown_database(e):
    """
    Teardown the Redis Database.

    Parameters
    ----------
    e : Exception
        The exception passed by the middleware during teardown process.
    """
    pass




