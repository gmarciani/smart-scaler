import redis


def create_connection(host, port):
    """
    Create a new connection to Redis.
    :param host: the hostname.
    :param port: the port number.
    :return: (Redis) the connection.
    """
    return redis.Redis(host, port)


def is_available(db):
    """
    Check the availability of the DB.
    :param db: the connection to DB.
    :return: True, if DB is available; False, otherwise.
    """
    try:
        db.get(None)
    except (redis.exceptions.ConnectionError,
            redis.exceptions.BusyLoadingError):
        return False
    return True


def get_value(db, key):
    return db.get(key)


def set_value(db, key, value):
    db.set(key, value)






