from flask import g
from uuid import getnode as get_mac
from os import getpid


def get_service_uid():
    """
    Return a UID for the current service instance.
    :return: (string) the UUID of the current service instance.
    """
    if not hasattr(g, "service_uid"):
        g.service_uid = _get_intance_uid()
    return g.service_uid


def _get_intance_uid():
    """
    Return a UID for the current service instance.
    :return: (string) the UUID of the current service instance.
    """
    return "{}__{}".format(get_mac(), getpid())


if __name__ == "__main__":
    print(_get_intance_uid())