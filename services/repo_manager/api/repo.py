import redis


def create_connection(host, port):
    """
    Create a new connection to Redis.
    :param host: (string) the DB hostname.
    :param port: (int) the DB port number.
    :return: (Redis) the connection.
    """
    return redis.Redis(host, port)


def is_available(db):
    """
    Check the availability of the DB.
    :param db: (connection) the connection to DB.
    :return: True, if DB is available; False, otherwise.
    """
    try:
        db.get(None)
    except (redis.exceptions.ConnectionError,
            redis.exceptions.BusyLoadingError):
        return False
    return True


def get_value(db, key):
    """
    Get the value of the specified key.
    :param db: (connection) the connection to DB.
    :param key: (string) the key.
    :return: (string) the value of the specified key, if present; None, otherwise.
    """
    return db.get(key)


def set_value(db, key, value):
    """
    Set the value of the specified key.
    :param db: (connection) the connection to DB.
    :param key: (string) the key.
    :param key: (string) the value.
    :return: (boolean) True, if succeeded; False, otherwise.
    """
    db.set(key, value)






