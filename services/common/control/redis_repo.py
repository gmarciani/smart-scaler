from services.common.model.exceptions.service_exception import RepositoryException
from services.common.model.ai.smart_scaling.smart_scaling_agent import SmartScalerQLearning
import redis
import redis_lock
import logging


# Configure logger
logger = logging.getLogger(__name__)


# Constants
LOCK_HEADER = "lock:"
SMART_SCALER_HEADER = "smart_scaler:"
CODEC = "UTF-8"


def create_connection(host, port):
    """
    Create an instance of a  Redis client.
    :param host: the hostname.
    :param port: the port number.
    :return: the Redis client.
    """
    return redis.StrictRedis(host=host, port=port, db=0)


def scan(r, pattern, decode=True):
    """
    Get all keys matching pattern.
    :param r: (Redis) the Redis Client.
    :param pattern: (str) the pattern.
    :param decode: (bool) if True, decode with CODEC.
    :return: (list) the list of keys.
    """
    try:
        result = r.scan(0, pattern)
    except redis.exceptions.ConnectionError as exc:
        raise RepositoryException(500, "get_key: " + str(exc))
    if decode:
        return list(x.decode(CODEC) for x in result[1])
    else:
        return result[1]


def get_key(r, key, decode=True):
    """
    Return the value for the key.
    :param r: (Redis) the Redis Client.
    :param key: (string) the key to retrieve the value of.
    :param decode: (bool) if True, decode with CODEC.
    :return: (string) the value for the key, if it exists; None, otherwise.
    """
    try:
        result = r.get(key)
    except redis.exceptions.ConnectionError as exc:
        raise RepositoryException(500, "get_key: " + str(exc))
    if result is not None and decode:
        return result.decode(CODEC)
    else:
        return result


def set_key(r, key, value, ttl=None, unique=False, existing=False):
    """
    Set the value for the key.
    :param r: (Redis) the Redis Client.
    :param key: (string) the key.
    :param value: (string) the value.
    :param ttl: (int) the TTL in seconds. If None no expiration is set.
    :param unique: (bool) if True, raises an error if key already exists.
    :param existing: (bool) if True, raises an error if key does not exists.
    :return: (boolean) True, if the key has been set; False, otherwise.
    """
    try:
        result = r.set(key, value, ex=ttl, nx=unique, xx=existing)
    except redis.exceptions.ConnectionError as exc:
        raise RepositoryException(500, "set_key: " + str(exc))
    return result


def set_ttl(r, key, ttl):
    """
    Set the TTL for the key.
    :param r: (Redis) the Redis Client.
    :param key: (string) the key.
    :param ttl: (int) the TTL in seconds. If None no expiration is set.
    :return: (boolean) True, if the TTL has been set; False, otherwise.
    """
    try:
        result = r.expire(key, ttl)
    except redis.exceptions.ConnectionError as exc:
        raise RepositoryException(500, "set_ttl: " + str(exc))
    return result


def delete_key(r, key):
    """
    Delete the key.
    :param r: (Redis) the Redis Client.
    :param key: (string) the key.
    :return: (boolean) True if succeeded; False, otherwise.
    """
    try:
        result = r.delete(key)
    except redis.exceptions.ConnectionError as exc:
        raise RepositoryException(500, "delete_key: " + str(exc))
    return result == 1


def load_smart_scaler(r, name):
    """
    Load the Smart Scaler with the specified name, if exists.
    :param r: an active Redis client.
    :param name: (str) the Smart Scaler name.
    :return: (SmartScaler) the Smart Scaler.
    """
    ss_binarys = get_key(r, "{}{}".format(SMART_SCALER_HEADER, name), decode=False)

    if ss_binarys is None:
        return None

    return SmartScalerQLearning.from_binarys(ss_binarys)


def store_smart_scaler(r, ss):
    """
    Store the Smart Scaler.
    :param r: an active Redis client.
    :param ss: (SmartScaler) the Smart Scaler.
    :return: None
    """
    ss_binarys = ss.to_binarys()
    set_key(r, "{}{}".format(SMART_SCALER_HEADER, ss.resource.name), ss_binarys)


def lock_smart_scaler(r, name, auid=None, expire=None):
    """
    Lock activities on the Smart Scaler with the specified name.
    :param r: an active Redis client.
    :param name: (str) a Smart Scaler name.
    :param auid: (str) the Agent Unique ID. Default is None.
    :param expire: (int) the expiration timeout, in seconds. Default is None.
    :return: (bool) True if the lock has been acquired; False, otherwise.
    """
    #return redis_lock.Lock(r, name, id=auid.encode(CODEC), expire=expire, auto_renewal=False)
    return redis_lock.Lock(r, name, id=None, expire=expire, auto_renewal=False)


def lock_reconciliation(r, auid=None, expire=None):
    """
    Lock activities of Repository Reconciliation.
    :param r: an active Redis client.
    :param auid: (str) the Agent Unique ID. Default is None.
    :param expire: (int) the expiration timeout, in seconds. Default is None.
    :return: (bool) True if the lock has been acquired; False, otherwise.
    """
    #return redis_lock.Lock(r, "system_reconciliation", id=auid.encode(CODEC), expire=expire, auto_renewal=False)
    return redis_lock.Lock(r, "system_reconciliation", id=None, expire=expire, auto_renewal=False)


def reconcile(r, names):
    """
    Delete all Smart Scalers whose names are not in 'names'.
    :param r: (Redis) the Redis Client.
    :param names: (set) the set of names.
    :return: (str) the name of deleted Smart Scalers.
    """
    names_all = list(map(lambda x: x.replace(SMART_SCALER_HEADER, ""), scan(r, "{}*".format(SMART_SCALER_HEADER))))

    ss_names_to_delete = list(filter(lambda n: n not in names, names_all))

    if len(ss_names_to_delete) == 0:
        return []

    pipe = r.pipeline()
    for n in ss_names_to_delete:
        pipe.delete("{}{}".format(SMART_SCALER_HEADER, n))
        pipe.delete("{}{}".format(LOCK_HEADER, n))
    result = pipe.execute()

    deleted = list()
    for i in range(len(ss_names_to_delete)):
        if result[i] is True:
            deleted.append(ss_names_to_delete[i])

    return deleted