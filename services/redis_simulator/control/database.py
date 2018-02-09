_DATABASE = {}


def get_database():
    """
    Retrieve the database.
    :return: (dict) the database.
    """
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
    pass
    #db = getattr(g, "_database", None)
    #if db is not None:
    #   db.close()


def __init_database():
    """
    Create a new database instance.
    :return: the new database instance.
    """
    return dict()

