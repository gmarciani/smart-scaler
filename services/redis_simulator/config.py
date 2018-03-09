"""
Configurations for the service 'Redis Simulator'.
"""


class Default:

    """
    Default configuration.
    """
    DEBUG = True

    LOG_LEVEL = "INFO"

    REPOSITORY_HOST = "localhost"
    REPOSITORY_PORT = 18009


class Debug(Default):
    """
    Debug configuration.
    """
    DEBUG = True

    LOG_LEVEL = "DEBUG"


class Production(Default):
    """
    Production configuration.
    """
    DEBUG = False
