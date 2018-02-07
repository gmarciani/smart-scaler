from flask import g

_DATABASE = {}


def get_database():
    """
    Retrieve the database.
    :return: (dict) the database.
    """
    return _DATABASE
    #db = getattr(g, "_database", None)
    #if db is None:
    #    pass
    #    #db = g._database = connect()
    #return db


def teardown_database(exc):
    """
    Teardown the database.
    :param exc: the optional exception
    :return: None
    """
    db = getattr(g, "_database", None)
    if db is not None:
        pass
        # TODO db.close()


def __init_database():
    """
    Create a new database instance.
    :return: the new database instance.
    """
    print("Init DB")
    return dict()

