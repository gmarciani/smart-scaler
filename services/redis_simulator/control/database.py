from services.redis_simulator.model.database import init_database
import logging

# Configure logger
logger = logging.getLogger(__name__)


_DATABASE = init_database()


def get_database():
    """
    Retrieve the database.
    :return: (dict) the database.
    """
    #logger.debug("Getting DB")
    return _DATABASE
    #db = getattr(g, "_database", None)
    #if db is None:
    #    #db = g._database = db_connect()
    #return db


def teardown_database(exc):
    """
    Teardown the database.
    :param exc: the exception passed by the middleware during teardown process.
    :return: None
    """
    #logger.debug("Tearing down DB")
    pass
    #db = getattr(g, "_database", None)
    #if db is not None:
    #   db.close()




