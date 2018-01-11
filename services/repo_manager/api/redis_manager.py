import redis


def is_redis_available(rconn):
    try:
        rconn.get(None)
    except (redis.exceptions.ConnectionError,
            redis.exceptions.BusyLoadingError):
        return False
    return True


def increment(rconn, key):
    return rconn.incr(key)


def get_value(rconn, key):
    return rconn.get(key)